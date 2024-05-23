<br/><br/><p align="center">
  <img src="https://lirp.cdn-website.com/c10be9aa/dms3rep/multi/opt/Optiorix+full+transparant+background+-+blue-c6d680b3-1920w.png" width="250"/>
</p><br/><br/>

# Introduction to Dimmy Webhooks
Webhooks are how services notify each other of events. At their core they are just a  `POST`  request to a pre-determined endpoint. The endpoint can be whatever you want, and you can just add them from our web application. You normally use one endpoint per service, and that endpoint listens to all of the event types. For example, if you receive webhooks from Acme Inc., you can structure your URL like:  `https://www.example.com/acme/webhooks/`.

This minimal Flask application serves as an illustration of what your webhook endpoint has to do. For incoming `items.scanned` events, this app verifies the payload using the request headers and your endpoint ***secret***. We also illustrate how you can use the webhook's item IDs to gather information about the incoming scanned objects using the Dimmy API. 

Note that this process is similar for languages other than Python. For payload verification in other languages, please refer to their excellent [documentation](https://docs.svix.com/receiving/verifying-payloads/how).

## Setting up webhooks 
To set up webhooks, you will need to navigate to the ***Webhook Dashboard***, which is accessible through ***Account & Limits*** in the [Dimmy Webapp](https://dimmy.app.optioryx.com/settings/account).

![Webhooks](/img/webhooks.png)

In the webhooks dashboard, you will be greeted with the endpoints page.

![Add endpoint](/img/new_endpoint.png)

You can click the "Add Endpoint" button to add your new endpoint. In production, you will deploy your endpoint to a domain or IP that is accessible [by our webhook workers](https://docs.optioryx.com/dimmy-webhooks), but for debugging, you can use the [Svix CLI](https://github.com/svix/svix-cli?tab=readme-ov-file#installation) to forward a "playground" endpoint to your localhost. After installing the CLI, we start our Flask application:
```
python main.py
``` 
Assuming our application is running on `http://127.0.0.1:5000` (should be visible in the output of the above command) and your webhook endpoint lives at `/webhook` (which is the case in this example), we can run 
```
svix listen http://127.0.0.1:5000/webhook
```
From the output of this command, we can find a webhook URL that will redirect any callbacks to our local machine.

![Forward](/img/svix_forward.png)

In the "Add Endpoint" screen that we navigated to earlier, we can now fill in the relay URL and select the event types that we will be listening to (in this case `items.scanned`).

![Forward](/img/svix_endpoint_create.png)

After creating the endpoint, we can reveal the signing secret used to verify that this call actually originates from our servers. The variable `secret` in `main.py` should be equal to this text (don't forget to restart your Flask app after any changes).

![Forward](/img/signing_secret.png)

## Setting up the Dimmy API
Your app is now ready to receive events that contain the unique IDs of objects that were just scanned. To reveal all information that was collected, we need to use this ID and a secret API key to query the [Dimmy API](https://dimmy.api.optioryx.com).

To create an API key, you will again need to navigate to the ***Account & Limits*** page in the [Dimmy Webapp](https://dimmy.app.optioryx.com/settings/account) and look for the "New API Key" button. The variable `dimmy_api_key` in `main.py` should be set to your API key (don't forget to restart your Flask app after any changes).

![Forward](/img/api_keys.png)

## Trying it out
Once `main.py` contains all necessary tokens, you're ready to receive events! Try to scan an object using the iOS app with an active internet connection and observe your Flask console's output. You should see the data you've just scanned in the JSON format specified by our [API docs](https://docs.optioryx.com/docs/dimmy-api/latest/get-items-items-get). 

On the webhook dashboard page for your endpoint, you should also see a log of requests. This allows for manual replay ([although requests are also retried automatically at various time intervals](https://docs.optioryx.com/dimmy-webhooks)). To test this out, you could try to intentionally add a fatal error to your endpoint in `main.py`, scan an object, fix the error and click replay in the dashboard. The event system will only mark an event as handled if your endpoint responds with a `20X` response code.

![Forward](/img/replay.png)
