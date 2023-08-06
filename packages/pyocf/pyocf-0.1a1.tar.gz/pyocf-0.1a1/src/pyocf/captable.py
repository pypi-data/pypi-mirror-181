import json
import pathlib
import zipfile

from pyocf import files
from pyocf.objects.stakeholder import Stakeholder
from pyocf.objects.stockclass import StockClass
from pyocf.objects.stocklegendtemplate import StockLegendTemplate
from pyocf.objects.stockplan import StockPlan
from pyocf.objects.transactions.acceptance.convertibleacceptance import (
    ConvertibleAcceptance,
)
from pyocf.objects.transactions.acceptance.plansecurityacceptance import (
    PlanSecurityAcceptance,
)
from pyocf.objects.transactions.acceptance.stockacceptance import StockAcceptance
from pyocf.objects.transactions.acceptance.warrantacceptance import WarrantAcceptance
from pyocf.objects.transactions.cancellation.convertiblecancellation import (
    ConvertibleCancellation,
)
from pyocf.objects.transactions.cancellation.plansecuritycancellation import (
    PlanSecurityCancellation,
)
from pyocf.objects.transactions.cancellation.stockcancellation import StockCancellation
from pyocf.objects.transactions.cancellation.warrantcancellation import (
    WarrantCancellation,
)
from pyocf.objects.transactions.conversion.convertibleconversion import (
    ConvertibleConversion,
)
from pyocf.objects.transactions.conversion.stockconversion import StockConversion
from pyocf.objects.transactions.exercise.plansecurityexercise import (
    PlanSecurityExercise,
)
from pyocf.objects.transactions.exercise.warrantexercise import WarrantExercise
from pyocf.objects.transactions.issuance.convertibleissuance import ConvertibleIssuance
from pyocf.objects.transactions.issuance.plansecurityissuance import (
    PlanSecurityIssuance,
)
from pyocf.objects.transactions.issuance.stockissuance import StockIssuance
from pyocf.objects.transactions.issuance.warrantissuance import WarrantIssuance
from pyocf.objects.transactions.reissuance.stockreissuance import StockReissuance
from pyocf.objects.transactions.release.plansecurityrelease import PlanSecurityRelease
from pyocf.objects.transactions.repurchase.stockrepurchase import StockRepurchase
from pyocf.objects.transactions.retraction.convertibleretraction import (
    ConvertibleRetraction,
)
from pyocf.objects.transactions.retraction.plansecurityretraction import (
    PlanSecurityRetraction,
)
from pyocf.objects.transactions.retraction.stockretraction import StockRetraction
from pyocf.objects.transactions.retraction.warrantretraction import WarrantRetraction
from pyocf.objects.transactions.split.stockclasssplit import StockClassSplit
from pyocf.objects.transactions.transfer.convertibletransfer import ConvertibleTransfer
from pyocf.objects.transactions.transfer.plansecuritytransfer import (
    PlanSecurityTransfer,
)
from pyocf.objects.transactions.transfer.stocktransfer import StockTransfer
from pyocf.objects.transactions.transfer.warranttransfer import WarrantTransfer
from pyocf.objects.transactions.vesting.vestingevent import VestingEvent
from pyocf.objects.transactions.vesting.vestingstart import VestingStart
from pyocf.objects.valuation import Valuation
from pyocf.objects.vestingterms import VestingTerms

FILEMAP = [
    ("stock_plans", files.stockplansfile.StockPlansFile),
    ("stock_legend_templates", files.stocklegendtemplatesfile.StockLegendTemplatesFile),
    ("stock_classes", files.stockclassesfile.StockClassesFile),
    ("vesting_terms", files.vestingtermsfile.VestingTermsFile),
    ("valuations", files.valuationsfile.ValuationsFile),
    ("transactions", files.transactionsfile.TransactionsFile),
    ("stakeholders", files.stakeholdersfile.StakeholdersFile),
]


class Captable:

    manifest: files.ocfmanifestfile.OCFManifestFile = None
    stock_plans: list[StockPlan] = []
    stock_legend_templates: list[StockLegendTemplate] = []
    stock_classes: list[StockClass] = []
    vesting_terms: list[VestingTerms] = []
    valuations: list[Valuation] = []
    transactions: list[
        ConvertibleAcceptance
        | PlanSecurityAcceptance
        | StockAcceptance
        | WarrantAcceptance
        | ConvertibleCancellation
        | PlanSecurityCancellation
        | StockCancellation
        | WarrantCancellation
        | ConvertibleConversion
        | StockConversion
        | PlanSecurityExercise
        | WarrantExercise
        | ConvertibleIssuance
        | PlanSecurityIssuance
        | StockIssuance
        | WarrantIssuance
        | StockReissuance
        | StockRepurchase
        | PlanSecurityRelease
        | ConvertibleRetraction
        | PlanSecurityRetraction
        | StockRetraction
        | WarrantRetraction
        | StockClassSplit
        | ConvertibleTransfer
        | PlanSecurityTransfer
        | StockTransfer
        | WarrantTransfer
        | VestingStart
        | VestingEvent
    ] = []
    stakeholders: list[Stakeholder] = []

    @classmethod
    def load(cls, location):
        """Imports OCF data

        `location` needs to be a string or a pathlib.Path() pointing at a
        zipfile or directory containing the OCF files, or it must be a
        file-like object containing a zip-file.
        """
        captable = Captable()

        # Assume it's a zip file or path to a zip file
        try:
            inzipfile = zipfile.ZipFile(location)
            manifest = json.loads(inzipfile.read("Manifest.ocf.json"))
            captable.manifest = files.ocfmanifestfile.OCFManifestFile(**manifest)

            def file_factory(p):
                # Normalize the path:
                p = str(pathlib.Path(p))
                return inzipfile.open(p)

        except zipfile.BadZipfile:
            # OK, then, let's assume it's a Manifest file in a directory

            # Make sure it's a pathlib path
            path = pathlib.Path(location)

            with path.open("rt") as infile:
                manifest = json.load(infile)
                captable.manifest = files.ocfmanifestfile.OCFManifestFile(**manifest)
                basedir = path.parent

            def file_factory(p):
                return open(pathlib.Path(basedir, p))

        for filetype, fileob in FILEMAP:
            for file in getattr(captable.manifest, filetype + "_files"):
                infile = file_factory(file.filepath)
                items = fileob(**json.load(infile)).items
                getattr(captable, filetype).extend(items)

        return captable

    def _save_ocf_files(self, manifest_path, file_factory, pretty):
        with file_factory(manifest_path) as ocffile:
            jsonstr = self.manifest.json(exclude_unset=True)
            if pretty:
                jsonstr = json.dumps(json.loads(jsonstr), indent=4)
            ocffile.write(jsonstr.encode("UTF-8"))

        for filetype, fileob in FILEMAP:
            ocffilename = getattr(self.manifest, filetype + "_files", [])
            if ocffilename:
                ocffilename = getattr(self.manifest, filetype + "_files")[0].filepath
            else:
                ocffilename == filetype + ".ocf.json"

            # Normalize the path
            ocffilename = str(pathlib.Path(ocffilename))

            with file_factory(ocffilename) as ocffile:
                itemfile = fileob(items=getattr(self, filetype))
                jsonstr = itemfile.json(exclude_unset=True)
                if pretty:
                    jsonstr = json.dumps(json.loads(jsonstr), indent=4)
                ocffile.write(jsonstr.encode("UTF-8"))

    def save(self, location, manifest_path="Manifest.ocf.json", zip=True, pretty=True):
        """Save the captable to a zipfile or a directory

        This will create a default manifest, if one doesn't exist
        already. For each file type, only one file will be created.
        If several file names are specified only the first one
        will be used.
        """
        # TODO: if there is no manifest, make one

        if zip:
            # Attempt standard PKZIP deflation
            if zipfile._get_compressor(zipfile.ZIP_DEFLATED) is None:
                # Didn't work, don't compress it
                compression = zipfile.ZIP_STORED
            else:
                compression = zipfile.ZIP_DEFLATED

            with zipfile.ZipFile(
                location, mode="w", compression=compression
            ) as outzipfile:
                self.save_zipfile(outzipfile, pretty=pretty)

        else:
            path = pathlib.Path(location).absolute()
            # Make sure it exists (and is a directory)
            # This gives good error messages if not a valid directory path
            path.mkdir(exist_ok=True)
            self.save_directory(path, pretty=pretty)

    def save_zipfile(self, outzipfile, manifest_path="Manifest.ocf.json", pretty=True):
        """Save to an already open zipfile

        Useful if you require non-standard compression or other zipfile options,
        then you can open the zipfile yourself and use this function to save to it.
        This function also requires you to setup the Manifest correctly.
        """

        def file_factory(p):
            return outzipfile.open(p, mode="w")

        self._save_ocf_files(manifest_path, file_factory, pretty)

    def save_directory(
        self, outdirectory, manifest_path="Manifest.ocf.json", pretty=True
    ):
        """Save to an already open zipfile

        Useful if you require non-standard compression or other zipfile options,
        then you can open the zipfile yourself and use this function to save to it.
        This function also requires you to setup the Manifest correctly.
        """

        def file_factory(p):
            return open(pathlib.Path(outdirectory, p), mode="wb")

        self._save_ocf_files(manifest_path, file_factory, pretty)
