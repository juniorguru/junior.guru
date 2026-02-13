from datetime import date
from typing import Callable

from jg.coop.models.transaction import TransactionsCategory


CATEGORIES_SPEC = []


def category_rule(rule: Callable):
    CATEGORIES_SPEC.append(rule)


@category_rule
def video_outsourcing(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["account_number_full"] in [
        "670100-2210965651/6210",
        "334772289/0300",
    ]:
        return TransactionsCategory.PRODUCTION
    token = secrets.get("video_outsourcing_token")
    if token and token in transaction["message"]:
        return TransactionsCategory.PRODUCTION


@category_rule
def membership_by_invoice(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["variable_symbol"] in ["21", "243", "241", "215"]:
        return TransactionsCategory.MEMBERSHIPS


@category_rule
def pavlun(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "pavlun" in transaction["message"] and transaction["amount"] < 0:
        return TransactionsCategory.PRODUCTION
    if "doniocz" in transaction["message"] and transaction["amount"] == 6180:
        return TransactionsCategory.PRODUCTION


@category_rule
def geekpower(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "geekpower" in transaction["message"].lower() and transaction["amount"] < 0:
        return TransactionsCategory.PRODUCTION


@category_rule
def frontendisti_honorarium(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "FRONTENDISTICZ" in transaction["message"] and transaction["amount"] > 0:
        return TransactionsCategory.DONATIONS


@category_rule
def tdc_conference_booth(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "Dan Srb, stánek" in transaction["message"] and transaction["amount"] < 0:
        return TransactionsCategory.MARKETING


@category_rule
def belabel(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "belabel.cz" in transaction["message"] and transaction["amount"] < 0:
        return TransactionsCategory.MARKETING


@category_rule
def podcasty_cz_commission(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "SKLIK" in transaction["message"] and "SEZNAM" in transaction["message"]:
        return TransactionsCategory.DONATIONS


@category_rule
def mews_sponsorship_2022(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["variable_symbol"] == "226":
        return TransactionsCategory.SPONSORSHIPS


@category_rule
def salary(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "výplata" in transaction["message"]:
        return TransactionsCategory.IGNORE


@category_rule
def cashflow(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "keš na cashflow" in transaction["message"]:
        return TransactionsCategory.IGNORE


@category_rule
def sideline(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["variable_symbol"] == "15":
        return TransactionsCategory.IGNORE


@category_rule
def sideline_apify(transaction: dict, secrets: dict) -> TransactionsCategory:
    if (
        transaction["variable_symbol"]
        and "Apify Technologies" in transaction["message"]
        and transaction["amount"] > 0
    ):
        return TransactionsCategory.IGNORE


@category_rule
def double_payment_by_mistake(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["date"] == date(2023, 9, 7) and transaction["amount"] == 12753:
        return TransactionsCategory.IGNORE
    if transaction["date"] == date(2023, 10, 20) and transaction["amount"] == -12753:
        return TransactionsCategory.IGNORE


@category_rule
def success_stories_writing(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["date"] == date(2023, 10, 30) and transaction["amount"] == 6180:
        return TransactionsCategory.PRODUCTION


@category_rule
def podcast_production(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "PAVLINA FRONKOVA" in transaction["message"]:
        return TransactionsCategory.PRODUCTION


@category_rule
def lawyer(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "ADVOKATKA" in transaction["message"]:
        return TransactionsCategory.LAWYER


@category_rule
def marketing_consultation(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "JANA DOLEJSOVA" in transaction["message"]:
        return TransactionsCategory.MARKETING


@category_rule
def accounting(transaction: dict, secrets: dict) -> TransactionsCategory:
    if (
        "Irein" in transaction["message"] or "účetnictví" in transaction["message"]
    ) and transaction["amount"] < 0:
        return TransactionsCategory.ACCOUNTING


@category_rule
def office(transaction: dict, secrets: dict) -> TransactionsCategory:
    message = transaction["message"].lower()
    if (
        "vitezslav pliska" in message
        or "vítek pliska" in message
        or "vitek pliska" in message
        or "creatiweb" in message
    ) and transaction["amount"] < 0:
        return TransactionsCategory.OFFICE


@category_rule
def discord(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "DISCORD" in transaction["message"] and transaction["amount"] < 0:
        return TransactionsCategory.DISCORD


@category_rule
def memberful(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "MEMBERFUL" in transaction["message"] and transaction["amount"] < 0:
        return TransactionsCategory.MEMBERFUL


@category_rule
def red_hat_sponsorships(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "RED HAT" in transaction["message"] and transaction["amount"] >= 8000:
        return TransactionsCategory.SPONSORSHIPS


@category_rule
def tax_social_care(transaction: dict, secrets: dict) -> TransactionsCategory:
    if (
        "ČSSZ" in transaction["message"]
        or "PSSZ" in transaction["message"]
        or "MSSZ" in transaction["message"]
    ):
        return TransactionsCategory.TAX


@category_rule
def tax_health_care(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "VZP" in transaction["message"]:
        return TransactionsCategory.TAX


@category_rule
def tax(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "FÚ pro hl. m. Prahu" in transaction["message"]:
        return TransactionsCategory.TAX


@category_rule
def tax_prepayments_and_payments(
    transaction: dict, secrets: dict
) -> TransactionsCategory:
    if transaction["bank_code"] == "0710" and transaction["amount"] < 0:
        return TransactionsCategory.TAX


@category_rule
def buffer_com(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "BUFFER PUBLISH" in transaction["message"] and transaction["amount"] < 0:
        return TransactionsCategory.MARKETING


@category_rule
def printall(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "printall" in transaction["message"].lower() and transaction["amount"] < 0:
        return TransactionsCategory.MARKETING


@category_rule
def stickers(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "samolep" in transaction["message"] and transaction["amount"] < 0:
        return TransactionsCategory.MARKETING


@category_rule
def pyconcz_2024_wisdom_board_stationery(
    transaction: dict, secrets: dict
) -> TransactionsCategory:
    if "PyCon CZ" in transaction["message"] and transaction["amount"] < 0:
        return TransactionsCategory.MARKETING


@category_rule
def github_sponsors(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "GITHUB SPONSORS" in transaction["message"] and transaction["amount"] > 0:
        return TransactionsCategory.DONATIONS


@category_rule
def memberships(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "STRIPE" in transaction["message"] and transaction["amount"] > 0:
        return TransactionsCategory.MEMBERSHIPS


@category_rule
def patreon(transaction: dict, secrets: dict) -> TransactionsCategory:
    if "PAYPAL" in transaction["message"] and transaction["amount"] > 0:
        return TransactionsCategory.DONATIONS


@category_rule
def direct_donations_fallback(transaction: dict, secrets: dict) -> TransactionsCategory:
    if not transaction["variable_symbol"] and transaction["amount"] > 0:
        return TransactionsCategory.DONATIONS


@category_rule
def direct_donations(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["variable_symbol"] == "444222" and transaction["amount"] > 0:
        return TransactionsCategory.DONATIONS


@category_rule
def sponsorships_fallback(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["variable_symbol"] and transaction["amount"] >= 8000:
        return TransactionsCategory.SPONSORSHIPS


@category_rule
def jobs_fallback(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["variable_symbol"] and transaction["amount"] > 0:
        return TransactionsCategory.JOBS


@category_rule
def default_fallback(transaction: dict, secrets: dict) -> TransactionsCategory:
    if transaction["amount"] > 0:
        return TransactionsCategory.DONATIONS
    return TransactionsCategory.MISCELLANEOUS
