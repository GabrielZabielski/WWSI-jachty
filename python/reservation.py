import json
from collections import namedtuple
from datetime import datetime

import boto3

from shared.jacht import Jacht
from shared.common_functions import get_jacht, get_email


def lambda_handler(event, context):
    if "id" in event.keys():
        jacht_id = event["id"]
    else:
        return {
            "statusCode": 401,
            'body': "<b>request doesn't contain information about requested jacht</b><br>Please, go back and try again."
        }
    jacht = get_jacht(jacht_id)[0]

    # GET
    if "method" not in event.keys():
        return {
            'statusCode': 200,
            'body': jacht_html(jacht)
        }

    # Make reservation
    if event["method"].__contains__("post"):
        try:
            date_check(jacht["reservation"], event["od"], event["do"])
        except Exception as ex:
            print(ex)
            return {
                'statusCode': 401,
                'body': json.dumps(str(ex))
            }
        try:
            email = get_email(event["access_token"])
            make_reservation(jacht, event["od"], event["do"], email)
        except Exception as ex:
            print(ex)
            return {
                'statusCode': 501,
                'body': json.dumps(str(ex))
            }

        return {
            'statusCode': 200,
            'body': json.dumps(f"Rezerwacja zakończona pomyślnie! Na twój adres {email} zostałby przesłany "
                               "rachunek i potwierdzenie, gdyby nie to, że amazon nie nie chce mi dać pełnej "
                               "wersji ich 'Simple email Service', która pozwala tak o wysyłać mejle", ensure_ascii=False)
        }

    elif event["method"].__contains__("delete"):
        related_reservation = {
            "od": event["od"],
            "do": event["do"],
            "email": get_email(event["access_token"])
        }
        delete_reservation(jacht, related_reservation)
        return {
            'statusCode': 200,
            'body': json.dumps("Rezerwacja została usunięta", ensure_ascii=False)
        }


def delete_reservation(jacht: dict, reservation):
    client = boto3.resource('dynamodb').Table("jachty")
    jacht_obj = Jacht(jacht)
    jacht_obj.remove_reservation(reservation)
    response = client.put_item(
        Item=jacht_obj.get_item()
    )


def make_reservation(jacht, od, do, email):
    client = boto3.resource('dynamodb').Table("jachty")
    jacht_obj = Jacht(jacht)
    jacht_obj.set_new_reservation(od=od, do=do, email=email)

    response = client.put_item(
        Item=jacht_obj.get_item()
    )


def date_check(reservations: list, od, do):
    od = datetime.fromisoformat(od)
    do = datetime.fromisoformat(do)
    if not datetime.now() < od < do:
        raise Exception("Provided invalid date frame")
    Range = namedtuple('Range', ['start', 'end'])
    ir = Range(start=od, end=do)
    for r in reservations:
        rr = Range(start=datetime.fromisoformat(r["od"]), end=datetime.fromisoformat(r["do"]))
        latest_start = max(ir.start, rr.start)
        earliest_end = min(ir.end, rr.end)
        delta = (earliest_end - latest_start).days + 1
        overlap = max(0, delta)
        if overlap != 0:
            raise Exception("Provided invalid date frame")


# view
def jacht_html(j: dict):
    reservations = []
    if j["reservation"]:
        for res in j["reservation"]:
            reservations.append(f"{res['od']} - {res['do']}")

    return f"""
<div class=jacht>
    <h3>{j["name"]}<h3>
    Cena za dzień: {j["price"]} zł
    <p>Porywający opis: {j["desc"]}
    <div class="row">
        <div class="column">
        <img src="https://s3.eu-central-1.amazonaws.com/jachty.gzabielski.click/picks/{j['jacht']}/0.jpg" style="width:100%">
        </div>
        <div class="column">
        <img src="https://s3.eu-central-1.amazonaws.com/jachty.gzabielski.click/picks/{j['jacht']}/1.jpg" style="width:100%">
        </div>
        <div class="column">
        <img src="https://s3.eu-central-1.amazonaws.com/jachty.gzabielski.click/picks/{j['jacht']}/2.jpg" style="width:100%">
        </div>
	</div>
<div class="row">
    <div class="column">
                <h3>Wybierz datę:</h3>
    <form id="rform" name="rform">
      <label for="od">Od:</label>
      <input type="text" id="_od" name="_od" value="2022-01-04"><br>
      <label for="do">Do:</label>
      <input type="text" id="_do" name="_do" value="2022-01-08"><br>
    </form> 
    	<button id="reserv" class="button button1">Zarezerwuj</button>
    </div>

    <div class="column">
    <h3>Zarezerwowane terminy: </h3>
    {'<br>'.join(reservations) if reservations else "Brak!"}
    </div>
</div>

</div>
    """
