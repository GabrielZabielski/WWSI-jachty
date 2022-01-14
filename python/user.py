import json
from shared.common_functions import get_jacht, get_email


def lambda_handler(event, context):
    try:
        email = get_email(event["access_token"])
    except Exception as ex:
        print(ex)
        return {
            'statusCode': 501,
            'body': json.dumps(str(ex))
        }
    user_reservations = get_user_reservations(email)

    return {
        'statusCode': 200,
        'body': user_html(user_reservations, email)
    }


def get_user_reservations(email):
    jachts = get_jacht()
    reservations = []
    for j in jachts:
        for reservation in j["reservation"]:
            if reservation["email"].__contains__(email):
                reservations.append(j)
                break
    return reservations


# view
def user_html(reservations: list, email: str):
    user_reservations = []
    for j in reservations:
        reserved = []
        if j["reservation"]:
            for res in j["reservation"]:
                if res["email"].__contains__(email):
                    reserved.append(
                        f"<div class='cancel' id='{j['jacht']}' data-od='{res['od']}' data-do='{res['do']}'>"
                        f"<h5 style='color:red;'>{res['od']} - {res['do']} | kliknij aby odwołać</h5></div>"
                    )
        if reserved:
            user_reservations.append(f"""
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
    	<button id="reserv" class="button button1">Zarezerwuj ponownie</button>
    </div>

    <div class="column">
    <h3>Zarezerwowane terminy: </h3>
    {"<br>".join(reserved)}
    </div>
</div>

</div>
    """)
    if user_reservations:
        return "\n".join(user_reservations)
    else:
        return "<h1>Czekamy na pierwszą rezerwację!</h1>"
