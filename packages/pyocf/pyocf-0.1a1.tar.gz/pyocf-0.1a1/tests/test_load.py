import datetime
import decimal
import json

from pathlib import Path
from pyocf.files import (
    ocfmanifestfile,
    stakeholdersfile,
    stockclassesfile,
    stocklegendtemplatesfile,
    stockplansfile,
    transactionsfile,
    valuationsfile,
    vestingtermsfile,
)
from pyocf.captable import Captable
from pyocf.objects import (
    transactions,
    stockplan,
    stakeholder,
    stockclass,
    stocklegendtemplate,
    valuation,
    vestingterms,
)
from pyocf.types import file, name, monetary, vesting
from pyocf.enums import (
    ocfversiontype,
    stockclasstype,
    allocationtype,
    vestingdayofmonth,
)

sample_path = Path(Path(__file__).parent.parent, "Open-Cap-Format-OCF/samples")


def test_load_sample_manifest():
    path = Path(Path(__file__).parent, Path(sample_path, "Manifest.ocf.json"))
    with path.open("rt") as infile:
        obj = ocfmanifestfile.OCFManifestFile(**json.load(infile))

    assert obj.ocf_version == ocfversiontype.OCFVersionType.ENUM_100a3
    assert obj.comments == ["This is an optional comment"]
    assert len(obj.stakeholders_files) == 1
    assert isinstance(obj.stakeholders_files[0], file.File)


def test_load_sample_stakeholders():
    path = Path(Path(__file__).parent, Path(sample_path, "Stakeholders.ocf.json"))
    with path.open("rt") as infile:
        obj = stakeholdersfile.StakeholdersFile(**json.load(infile))
    assert len(obj.items) == 2
    item = obj.items[0]
    assert isinstance(item, stakeholder.Stakeholder)
    assert item.object_type == "STAKEHOLDER"
    assert isinstance(item.name, name.Name)


def test_load_sample_stock_classes():
    path = Path(Path(__file__).parent, Path(sample_path, "StockClasses.ocf.json"))
    with path.open("rt") as infile:
        obj = stockclassesfile.StockClassesFile(**json.load(infile))

    assert len(obj.items) == 2
    item = obj.items[0]
    assert isinstance(item, stockclass.StockClass)
    assert item.object_type == "STOCK_CLASS"
    assert item.name == "Common Stock"
    assert item.class_type == stockclasstype.StockClassType.ENUM_COMMON
    assert isinstance(item.par_value, monetary.Monetary)
    assert item.par_value.currency == "USD"
    assert item.par_value.amount == decimal.Decimal("0.0001000000")

    item = obj.items[1]
    assert item.class_type == stockclasstype.StockClassType.ENUM_PREFERRED


def test_load_sample_stock_legend_templates():
    path = Path(Path(__file__).parent, Path(sample_path, "StockLegends.ocf.json"))
    with path.open("rt") as infile:
        obj = stocklegendtemplatesfile.StockLegendTemplatesFile(**json.load(infile))

    assert len(obj.items) == 1
    item = obj.items[0]
    assert isinstance(item, stocklegendtemplate.StockLegendTemplate)
    item.object_type == "STOCK_LEGEND_TEMPLATE"
    item.name == "1933 Act Legend"


def test_load_sample_stock_plans():
    path = Path(Path(__file__).parent, Path(sample_path, "StockPlans.ocf.json"))
    with path.open("rt") as infile:
        obj = stockplansfile.StockPlansFile(**json.load(infile))
    assert len(obj.items) == 1
    item = obj.items[0]
    assert isinstance(item, stockplan.StockPlan)
    assert item.object_type == "STOCK_PLAN"
    assert item.plan_name == "2021 Stock Incentive Plan"
    assert item.board_approval_date == datetime.date(1983, 12, 31)
    assert item.initial_shares_reserved == decimal.Decimal("10000000")
    assert item.stock_class_id == "8d8371e8-d41d-4a49-9f42-b91758fd155d"
    assert item.comments == [
        "Using new form of SOP released by Firm Y's benefits & comp team on 10/10/2021."
    ]


def test_load_sample_transactions():
    path = Path(Path(__file__).parent, Path(sample_path, "Transactions.ocf.json"))
    with path.open("rt") as infile:
        obj = transactionsfile.TransactionsFile(**json.load(infile))
    item = obj.items[0]
    assert isinstance(
        item, transactions.acceptance.convertibleacceptance.ConvertibleAcceptance
    )
    assert item.id == "test-convertible-acceptance-minimal"
    assert item.security_id == "2936wa8yefhdsvcn"
    assert item.object_type == "TX_CONVERTIBLE_ACCEPTANCE"
    assert item.date == datetime.date(2022, 1, 20)

    item = obj.items[62]
    assert isinstance(item, transactions.retraction.warrantretraction.WarrantRetraction)
    assert item.id == "test-warrant-retraction-full-fields"
    assert item.security_id == "test-security-id"
    assert item.object_type == "TX_WARRANT_RETRACTION"
    assert item.reason_text == "Need to retract"
    assert item.date == datetime.date(2022, 2, 1)
    assert item.comments == ["Here is a comment", "Here is another comment"]


def test_load_sample_valuations_files():
    path = Path(Path(__file__).parent, Path(sample_path, "Valuations.ocf.json"))
    with path.open("rt") as infile:
        obj = valuationsfile.ValuationsFile(**json.load(infile))

    assert len(obj.items) == 1
    item = obj.items[0]
    assert isinstance(item, valuation.Valuation)
    item.object_type == "VALUATION"
    item.valuation_type == "409A",


def test_load_sample_vesting_terms():
    path = Path(Path(__file__).parent, Path(sample_path, "VestingTerms.ocf.json"))
    with path.open("rt") as infile:
        obj = vestingtermsfile.VestingTermsFile(**json.load(infile))

    assert len(obj.items) == 5
    item = obj.items[0]
    assert isinstance(item, vestingterms.VestingTerms)
    item.object_type == "VESTING_TERMS"
    assert item.name == "Four Year / One Year Cliff"
    assert (
        item.allocation_type == allocationtype.AllocationType.ENUM_CUMULATIVE_ROUNDING
    )

    assert len(item.vesting_conditions) == 3
    assert isinstance(
        item.vesting_conditions[0], vesting.vestingcondition.VestingCondition
    )
    assert item.vesting_conditions[0].id == "vesting-start"
    assert item.vesting_conditions[0].next_condition_ids == ["cliff"]

    # Vesting conditions can have different trigger types
    condition = item.vesting_conditions[0]
    assert isinstance(
        condition.trigger, vesting.vestingstarttrigger.VestingStartTrigger
    )
    assert condition.portion is None

    condition = item.vesting_conditions[1]
    assert isinstance(
        condition.portion, vesting.vestingconditionportion.VestingConditionPortion
    )
    assert condition.portion.numerator == decimal.Decimal("12")
    assert condition.portion.denominator == decimal.Decimal("48")

    trigger = condition.trigger
    assert isinstance(
        trigger, vesting.vestingschedulerelativetrigger.VestingScheduleRelativeTrigger
    )
    assert isinstance(
        trigger.period, vesting.vestingperiodinmonths.VestingPeriodInMonths
    )
    assert trigger.period.length == 12
    assert trigger.period.occurrences == 1
    assert (
        trigger.period.day_of_month
        == vestingdayofmonth.VestingDayOfMonth.ENUM_VESTING_START_DAY_OR_LAST_DAY_OF_MONTH
    )

    condition = item.vesting_conditions[2]
    trigger = condition.trigger
    assert trigger.period.length == 1
    assert trigger.period.occurrences == 36

    item = obj.items[1]
    assert (
        item.allocation_type == allocationtype.AllocationType.ENUM_CUMULATIVE_ROUND_DOWN
    )
    assert len(item.vesting_conditions) == 8
    assert isinstance(
        item.vesting_conditions[0], vesting.vestingcondition.VestingCondition
    )
    assert item.vesting_conditions[0].id == "vesting-start"

    condition = item.vesting_conditions[1]
    assert condition.portion is None
    assert condition.quantity == 0

    condition = item.vesting_conditions[2]
    assert condition.portion.numerator == 1
    assert condition.portion.denominator == 1

    trigger = condition.trigger
    assert isinstance(trigger, vesting.vestingeventtrigger.VestingEventTrigger)
    assert trigger.type == "VESTING_EVENT"

    item = obj.items[3]
    assert item.allocation_type == allocationtype.AllocationType.ENUM_BACK_LOADED

    item = obj.items[4]
    condition = item.vesting_conditions[4]
    assert condition.quantity == 0
    assert isinstance(
        condition.trigger,
        vesting.vestingscheduleabsolutetrigger.VestingScheduleAbsoluteTrigger,
    )
    assert condition.trigger.date == datetime.date(2017, 4, 1)


def test_load_captable_directory():
    path = Path(Path(__file__).parent, Path(sample_path, "Manifest.ocf.json"))
    # Just check that each type of data is not empty, ie, that it has been loaded.
    # The above tests check that the loading works corrcetly.
    captable = Captable.load(path)
    assert captable.manifest
    assert captable.stakeholders
    assert captable.stock_classes
    assert captable.stock_legend_templates
    assert captable.stock_plans
    assert captable.transactions
    assert captable.valuations
    assert captable.vesting_terms


def test_load_captable_zipfile():
    path = Path(Path(__file__).parent, "samples/Captable.ocf.zip")
    # Just check that each type of data is not empty, ie, that it has been loaded.
    # The above tests check that the loading works corrcetly.
    captable = Captable.load(path)
    assert captable.manifest
    assert captable.stakeholders
    assert captable.stock_classes
    assert captable.stock_legend_templates
    assert captable.stock_plans
    assert captable.transactions
    assert captable.valuations
    assert captable.vesting_terms


def test_load_captable_filelike():
    path = Path(Path(__file__).parent, "samples/Captable.ocf.zip")
    # Just check that each type of data is not empty, ie, that it has been loaded.
    # The above tests check that the loading works corrcetly.
    with open(path, "rb") as file:
        captable = Captable.load(file)
    assert captable.manifest
    assert captable.stakeholders
    assert captable.stock_classes
    assert captable.stock_legend_templates
    assert captable.stock_plans
    assert captable.transactions
    assert captable.valuations
    assert captable.vesting_terms
