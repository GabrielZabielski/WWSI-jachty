from shared.common_functions import get_jacht


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': get_jacht_list(get_jacht())
    }


def get_jacht_list(j: list):
    if len(j) > 1:
        js = sorted(j, key=lambda i: i['jacht'])
    else:
        js = j
    jachts = []
    for x in js:
        link = f"'/get_jacht_page?jacht_id={x['jacht']}&access_token=' + urlParams.get('access_token')"
        jachts.append(f"""
<div class=jacht>
    <h3>{x["name"]}<h3>
    Cena za dzień: {x["price"]} zł
    <p>Porywający opis: {x["desc"]}
    <div class="row">
        <div class="column">
        <img src="https://s3.eu-central-1.amazonaws.com/jachty.gzabielski.click/picks/{x['jacht']}/0.jpg" style="width:100%">
        </div>
        <div class="column">
        <img src="https://s3.eu-central-1.amazonaws.com/jachty.gzabielski.click/picks/{x['jacht']}/1.jpg" style="width:100%">
        </div>
        <div class="column">
        <img src="https://s3.eu-central-1.amazonaws.com/jachty.gzabielski.click/picks/{x['jacht']}/2.jpg" style="width:100%">
        </div>
	</div>
	<button onclick="location.href={link}" class="button button2">Rezerwuj</button>
</div>
        """)
    return "<br>".join(jachts)
