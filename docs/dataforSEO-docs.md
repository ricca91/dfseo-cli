### JavaScript (Node.js): Get App Info Tasks Ready

Source: https://docs.dataforseo.com/v3/app_data/apple/app_info/tasks_ready

This Node.js example uses the `axios` library to make a GET request to the DataForSEO API. It demonstrates how to set up authentication using `auth` object with `username` and `password`, specify the endpoint for app info tasks, and handle the response or errors. Ensure `axios` is installed (`npm install axios`).

```javascript
const axios = require('axios');


axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/app_data/apple/app_info/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});

```

--------------------------------

### PHP Client Example for GET /v3/serp/bing/local_pack/tasks_ready

Source: https://docs.dataforseo.com/v3/serp/bing/local_pack/tasks_ready

Example usage of the DataForSEO API using a PHP RestClient. This snippet shows how to initialize the client, make a GET request to the tasks_ready endpoint, and handle potential errors.

```APIDOC
## PHP Client Example for GET /v3/serp/bing/local_pack/tasks_ready

### Description
This PHP code demonstrates how to use the provided RestClient to interact with the DataForSEO API. It includes initialization with credentials, making a GET request to retrieve task statuses, and error handling.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/serp/bing/local_pack/tasks_ready

### Parameters

#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {

    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

    $client = new RestClient($api_url, null, 'YOUR_LOGIN', 'YOUR_PASSWORD');

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

    exit();

}

try {

    // using this method you can get a list of completed tasks

    // GET /v3/serp/bing/local_pack/tasks_ready

    // in addition to 'bing' and 'local_pack' you can also set other search engine and type parameters

    // the full list of possible parameters is available in documentation

    $result = $client->get('/v3/serp/bing/local_pack/tasks_ready');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

### Response
#### Success Response (200)
- **Result** (mixed) - The response from the API, typically an array or object containing task results.

#### Response Example
```php
Array
(
    [tasks] => Array
        (
            [0] => Array
                (
                    [id] => 01032305-016a-05a2-0000-71706e930535
                    [status_code] => 2
                    [status_message] => ok
                    [time_spent] => 0.001s
                    [cost] => 0.0001
                    [result_url] => https://api.dataforseo.com/v3/serp/bing/local_pack/serp/01032305-016a-05a2-0000-71706e930535
                    [result] => Array
                        (
                            // ... task specific results ...
                        )

                )

        )

    [statistic] => Array
        (
            // ... statistic details ...
        )

)
```
```

--------------------------------

### Python Client Example for GET /v3/serp/bing/local_pack/tasks_ready

Source: https://docs.dataforseo.com/v3/serp/bing/local_pack/tasks_ready

This Python example uses a provided RestClient to fetch completed tasks from the DataForSEO API. It demonstrates simple initialization and making a GET request.

```APIDOC
## Python Client Example for GET /v3/serp/bing/local_pack/tasks_ready

### Description
This Python code snippet shows how to use the `RestClient` class to access the DataForSEO API. It initializes the client with credentials and makes a GET request to retrieve task statuses.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/serp/bing/local_pack/tasks_ready

### Parameters

#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
from client import RestClient

# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip

client = RestClient("YOUR_LOGIN", "YOUR_PASSWORD")

# using this method you can get a list of completed tasks

# GET /v3/serp/bing/local_pack/tasks_ready

# in addition to 'bing' and 'local_pack' you can also set other search engine and type parameters

# the full list of possible parameters is available in documentation

response = client.get("/v3/serp/bing/local_pack/tasks_ready")

print(response)
```

### Response
#### Success Response (200)
- **response** (dict) - The dictionary containing the API response, which includes task details and statistics.

#### Response Example
```python
{
    'tasks': [
        {
            'id': '01032305-016a-05a2-0000-71706e930535',
            'status_code': 2,
            'status_message': 'ok',
            'time_spent': '0.001s',
            'cost': 0.0001,
            'result_url': 'https://api.dataforseo.com/v3/serp/bing/local_pack/serp/01032305-016a-05a2-0000-71706e930535',
            'result': [
                # ... task specific results ...
            ]
        }
    ],
    'statistic': {
        # ... statistic details ...
    }
}
```
```

--------------------------------

### HTTP Request Setup using Java

Source: https://docs.dataforseo.com/v2/op_csharp=

This Java code snippet demonstrates the setup for making HTTP requests, including GET and POST methods, using the Apache HttpClient library. It imports necessary classes for handling HTTP responses, clients, methods, and entities. This code is foundational for interacting with web services.

```java
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;

```

--------------------------------

### Fetch Google Keywords Data - JavaScript (Node.js)

Source: https://docs.dataforseo.com/v3/keywords_data/google/keywords_for_site/tasks_ready

This JavaScript example uses the `axios` library to make a GET request to the Dataforseo API for fetching Google keywords data. It demonstrates how to set up the request URL, authentication, and headers. Ensure you have `axios` installed (`npm install axios`). Replace 'login' and 'password' with your actual API credentials.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/keywords_data/google/keywords_for_site/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Java HTTP Client Setup for DataForSeo API

Source: https://docs.dataforseo.com/v2/op_java=

This Java snippet shows the basic setup for an HTTP client to interact with the DataForSeo API. It configures an HttpClient and prepares a GET request, including a placeholder for authentication credentials. Note that the authentication part is not fully implemented in this snippet.

```java
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.util.*;
public class Demos {
    public static void op_tasks_get_broken_pages() throws JSONException, IOException {
        HttpClient client;
        client = HttpClientBuilder.create().build();
        int taskId = 123456789;
        HttpGet get = new HttpGet("https://api.dataforseo.com/v2/op_tasks_get_broken_pages/" + taskId);
        //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard

```

--------------------------------

### Node.js (Axios) Example for GET /v3/serp/bing/local_pack/tasks_ready

Source: https://docs.dataforseo.com/v3/serp/bing/local_pack/tasks_ready

This Node.js example utilizes the Axios library to make a GET request to the DataForSEO API's tasks_ready endpoint. It shows how to configure authentication and handle the response.

```APIDOC
## Node.js (Axios) Example for GET /v3/serp/bing/local_pack/tasks_ready

### Description
This Node.js code snippet demonstrates fetching completed tasks using the Axios HTTP client. It configures the request with Basic Authentication and processes the returned data.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/serp/bing/local_pack/tasks_ready

### Parameters

#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/bing/local_pack/tasks_ready',

    auth: {

        username: 'YOUR_LOGIN',

        password: 'YOUR_PASSWORD'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

### Response
#### Success Response (200)
- **result** (array) - The 'result' field from the first task in the response, containing the SERP analysis data.

#### Response Example
```json
[
  {
    "se_query_params": null,
    "items_count": 1,
    "spell_suggestion": null,
    "filter": null,
    "site_organic": [
      {
        "rank_changes": {
          "position_changes": 0,
          "last_update": 1643144000
        },
        "domain": "example.com",
        "title": "Example Domain",
        "breadcrumb": "Home > Example"
      }
    ]
  }
]
```
```

--------------------------------

### GET /v3/serp/google/ads_search/tasks_ready (Python)

Source: https://docs.dataforseo.com/v3/serp/google/ads_search/tasks_ready_php=

This Python example utilizes a RestClient to fetch completed tasks for Google Ads search. Ensure you have the `client` library installed or available.

```APIDOC
## GET /v3/serp/google/ads_search/tasks_ready

### Description
Retrieves a list of completed tasks for Google Ads search using the Python RestClient.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/serp/google/ads_search/tasks_ready

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```python
from client import RestClient

# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip

client = RestClient("login", "password")

# using this method you can get a list of completed tasks
response = client.get("/v3/serp/google/ads_search/tasks_ready")
```

### Response
#### Success Response (200)
- **tasks** (list) - A list of completed tasks.
  - **id** (str) - The ID of the task.
  - **result** (dict) - The result of the task.

#### Response Example
```python
{
    "tasks": [
        {
            "id": "01234567-89ab-cdef-0123-456789abcdef",
            "result": {
                "some_data": "example"
            }
        }
    ]
}
```
```

--------------------------------

### Get DataForSEO Labs Locations and Languages (C#)

Source: https://docs.dataforseo.com/v3/dataforseo_labs/locations_and_languages

This C# example demonstrates how to make a GET request to the DataForSEO Labs 'locations_and_languages' endpoint using `HttpClient` and `Newtonsoft.Json`. It includes authentication setup and response handling, checking for a success status code (20000) before processing the result.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_locations_and_languages()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of locations and languages

            // GET /v3/dataforseo_labs/locations_and_languages

            var response = await httpClient.GetAsync("/v3/dataforseo_labs/locations_and_languages");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Sandbox Live Endpoint Example (Domain Analytics, Labs, Backlinks)

Source: https://docs.dataforseo.com/v3/app_data/google/overview

This example illustrates using a sandbox 'live' endpoint. For APIs that deliver data directly via a live method, no separate GET request is needed after the initial POST.

```APIDOC
## GET /v3/domain_analytics/technologies/aggregation_technologies/live

### Description
This example shows how to access a 'live' endpoint in the sandbox environment. These endpoints deliver data directly, and no separate GET request is required to fetch results after the initial call.

### Method
GET

### Endpoint
https://sandbox.dataforseo.com/v3/domain_analytics/technologies/aggregation_technologies/live

### Parameters
No specific parameters mentioned for this example, but actual live endpoints may have query or POST parameters.

### Request Example
(Assuming a GET request for simplicity, actual implementation might involve POST with parameters)
```json
{
  "domain": "example.com"
}
```

### Response
#### Success Response (200)
- **status** (string) - The status of the request.
- **data** (object) - The response data from the sandbox API, containing dummy data.

#### Response Example
```json
{
  "status": "ok",
  "data": {
    "technologies": [
      {
        "name": "ExampleTechnology",
        "version": "1.0"
      }
    ]
  }
}
```
```

--------------------------------

### Fetch Google Keyword Ideas via Node.js

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live

This JavaScript example uses the 'axios' library to make a POST request to the Dataforseo API for live Google keyword ideas. It demonstrates how to set up authentication using basic auth, define the request payload with keywords, location, language, filters, and limit, and handle the response or errors. Make sure to install axios: `npm install axios`.

```javascript
const post_array = [];



post_array.push({

  "keywords": [

    "phone",

    "watch"

  ],

  "location_code": 2840,

  "language_name": "English",

  "filters": [["keyword_info.search_volume", ">", 10]] ,

  "limit": 3



});



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Make Authenticated API Request in C#

Source: https://docs.dataforseo.com/v3/serp/youtube/video_subtitles/tasks_fixed

This C# example shows how to set up an authenticated HTTP client to interact with the DataForSEO API. It configures the client with a base address and includes basic authentication using provided 'login' and 'password'. The example then makes a GET request to the 'serp/youtube/video_subtitles/tasks_fixed' endpoint and deserializes the JSON response.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_tasks_fixed()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/serp/youtube/video_subtitles/tasks_fixed

            // in addition to 'youtube' and 'video_subtitles' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/serp/youtube/video_subtitles/tasks_fixed");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Pingback URL Examples

Source: https://docs.dataforseo.com/v2/cmn/v2/rnk

Provides examples of pingback URLs that can be used to receive GET requests when a task is completed. It shows how to use task_id and post_id variables.

```url
http://your-server.com/pingscript?taskId=$task_id
```

```url
http://your-server.com/pingscript?taskId=$task_id&postId=$post_id
```

--------------------------------

### C#: Get Google Keywords for Site Live

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/keywords_for_site/live

This C# example demonstrates how to fetch live Google keywords using the Dataforseo Labs API. It sets up an HttpClient with authentication and constructs the request body with target, location, language, and filtering options. The code sends a POST request and deserializes the JSON response, handling success and error cases.

```csharp
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task dataforseo_labs_google_keyword_for_site_live()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };

            var postData = new List<object>();
            postData.Add(new
            {
                target = "apple.com",
                location_name = "United States",
                language_name = "English",
                include_serp_info = true,
                include_subdomains = true,
                limit = 3,
                filters = new object[]
                { "keyword_properties.keyword_difficulty", ">", 0 }
            });

            // POST /v3/dataforseo_labs/google/keywords_for_site/live
            // the full list of possible parameters is available in documentation
            var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/google/keywords_for_site/live", new StringContent(JsonConvert.SerializeObject(postData)));
            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
            if (result.status_code == 20000)
            {
                // do something with result
                Console.WriteLine(result);
            }
            else
                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");
        }
    }
}

```

--------------------------------

### Fetch Keywords for Site Live using C#

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/live_php=

This C# example demonstrates how to use the DataForSEO API to get live keyword data for a specific website. It sets up an HTTP client with authentication, constructs a POST request payload, sends it to the '/v3/keywords_data/google_ads/keywords_for_site/live' endpoint, and then processes the JSON response, checking for success or error codes. It utilizes Newtonsoft.Json for JSON serialization and deserialization.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_keywords_for_site_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))
                }

            };

            var postData = new List<object>();

            postData.Add(
                new
                {
                    location_name = "United States",

                    target = "dataforseo.com"
                }
            );

            // POST /v3/keywords_data/google_ads/keywords_for_site/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/keywords_data/google_ads/keywords_for_site/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Fetch Google Ads Search Volume Data using Node.js (axios)

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/tasks_ready

This Node.js example uses the 'axios' library to make a GET request to the Dataforseo API for Google Ads search volume data. It demonstrates how to set up authentication using the 'auth' object and includes basic handling for successful responses and errors. Ensure you have axios installed (`npm install axios`).

```javascript
const axios = require('axios');


axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get Task Results by Task ID using C#

Source: https://docs.dataforseo.com/v2/kwrd_finder_python=

This C# snippet outlines the initial setup for retrieving task results by task ID. It uses HttpClient to make requests to the DataForSeo API, requiring API credentials. The code is a starting point and would need further implementation to handle the full request and response. Ensure Newtonsoft.Json is installed.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task kwrd_finder_suggest_tasks_get_by_task_id()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard

```

--------------------------------

### Set up a dataforseo task with URL parameters and POST data callback

Source: https://docs.dataforseo.com/v3/serp/yahoo/organic/task_post

This example shows an alternative method for setting up a task where all required parameters are passed directly in the URL. It also configures the API to send results to a specified 'postback_url' in a 'postback_data' format upon task completion.

```python
post_data[len(post_data)] = dict(

    url="https://search.yahoo.com/search?p=rank+checker&n=100&vl=lang_en&vc=us&ei=UTF-8",

    postback_data="html",

    postback_url="https://your-server.com/postbackscript"

)
```

--------------------------------

### Setting Operating System (Example)

Source: https://docs.dataforseo.com/v3/serp/google/organic/task_post

Shows how to specify the target operating system for mobile or desktop. This is relevant when simulating specific device environments for data collection.

```json
{
  "os": "android"
}
```

```json
{
  "os": "macos"
}
```

--------------------------------

### Configure Task with URL Parameters and Postback (Python)

Source: https://docs.dataforseo.com/v3/serp/yahoo/organic/task_post_php=

This example demonstrates an alternative method for setting up a task by passing all required parameters directly within a URL. It also configures postback data and URL to receive results upon task completion. This approach is suitable when specific search engine and type parameters need to be embedded in the request.

```python
post_data = {}

post_data[len(post_data)] = dict(

    url="https://search.yahoo.com/search?p=rank+checker&n=100&vl=lang_en&vc=us&ei=UTF-8",

    postback_data="html",

    postback_url="https://your-server.com/postbackscript"

)

# POST /v3/serp/yahoo/organic/task_post
# Assuming 'client' is an initialized API client object
response = client.post("/v3/serp/yahoo/organic/task_post", post_data)
```

--------------------------------

### Fetch Ready App List Tasks using JavaScript (axios)

Source: https://docs.dataforseo.com/v3/app_data/google/app_list/tasks_ready

This JavaScript example utilizes the axios library to make a GET request to the DataForSEO API for fetching ready app list tasks. It demonstrates how to set up authentication, headers, and handle both successful responses and errors. Replace 'login' and 'password' with your credentials.

```javascript
const axios = require('axios');


axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/app_data/google/app_list/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch Keywords For Site Live using DataForSEO API (C#)

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/live

This C# example demonstrates how to use the DataForSEO API to fetch live keyword data for a given website. It includes setting up the HttpClient, authentication, constructing the POST request payload, sending the request, and deserializing the JSON response. Error handling is included by checking the status code.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_keywords_for_site_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                location_name = "United States",

                target = "dataforseo.com"

            });

            // POST /v3/keywords_data/google_ads/keywords_for_site/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/keywords_data/google_ads/keywords_for_site/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Fetch Lighthouse Tasks Ready (PHP)

Source: https://docs.dataforseo.com/v3/on_page/lighthouse/tasks_ready_php=

This PHP script utilizes the `RestClient` class to fetch lighthouse tasks that are ready from the DataForSEO API. It requires downloading the `php_RestClient.zip` example file. The script demonstrates authentication, making a GET request, and handling potential `RestClientException` errors. Replace 'login' and 'password' with your API credentials.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');



try {

   // using this method you can get a list of completed tasks

   // GET /v3/on_page/lighthouse/tasks_ready

   $result = $client->get('/v3/on_page/lighthouse/tasks_ready');

   print_r($result);

   // do something with result

} catch (RestClientException $e) {

   echo "n";

   print "HTTP code: {$e->getHttpCode()}n";

   print "Error code: {$e->getCode()}n";

   print "Message: {$e->getMessage()}n";

   print  $e->getTraceAsString();

   echo "n";

}

$client = null;

?>
```

--------------------------------

### Fetch Merchant Google Product Info Tasks Ready in C#

Source: https://docs.dataforseo.com/v3/merchant/google/product_info/tasks_ready

This C# example demonstrates how to use the HttpClient to make a GET request to the /v3/merchant/google/product_info/tasks_ready endpoint. It includes setting up authentication with provided credentials and deserializing the JSON response. The code handles success and error responses based on the 'status_code'.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task merchant_google_product_info_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/merchant/google/product_info/tasks_ready

            var response = await httpClient.GetAsync("/v3/merchant/google/product_info/tasks_ready");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Lighthouse Versions using Python

Source: https://docs.dataforseo.com/v3/on_page/lighthouse/versions

This Python example shows how to retrieve Lighthouse versions using a custom RestClient. It requires downloading the client zip file and then initializing the client with API credentials to make the GET request.

```python
from random import Random
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip


client = RestClient("login", "password")
# using this method you can get a list of available versions
# GET /v3/on_page/lighthouse/versions
response = client.get("/v3/on_page/lighthouse/versions")
```

--------------------------------

### Sandbox GET Request Example (Task-based APIs)

Source: https://docs.dataforseo.com/v3/app_data/google/overview

This example shows how to retrieve task results from a sandbox endpoint using a GET request. This is applicable to APIs that use a task ID system.

```APIDOC
## GET /v3/serp/google/organic/task_get/advanced/$id

### Description
This endpoint allows retrieving task results from the sandbox environment for APIs that operate on a task-based system. Replace `$id` with the actual task ID.

### Method
GET

### Endpoint
https://sandbox.dataforseo.com/v3/serp/google/organic/task_get/advanced/$id

### Parameters
#### Path Parameters
- **id** (string) - Required - The ID of the task for which to retrieve results.

### Request Example
```json
{
  "id": "00000000-0000-0000-0000-000000000000"
}
```

### Response
#### Success Response (200)
- **status** (string) - The status of the request.
- **data** (object) - The response data from the sandbox API, containing dummy data for the specified task.

#### Response Example
```json
{
  "status": "ok",
  "data": {
    "keyword": "example_query",
    "placeholder_field": "dummy_value"
  }
}
```
```

--------------------------------

### Get Google Locations List - Python

Source: https://docs.dataforseo.com/v3/reviews-google-locations

Initiates a request to get Google review locations using Python. This example assumes the use of a provided RestClient class for authentication and API interaction. It's a basic setup for fetching location data.

```python
from client import RestClient

# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip

client = RestClient("login", "password")

```

--------------------------------

### Get Google Shopping HTML Tasks by Task ID (Java)

Source: https://docs.dataforseo.com/v2/merchant_csharp=

Retrieves Google Shopping HTML task data using Java. This example utilizes Apache HttpClient for making HTTP GET requests and the org.json library for parsing JSON responses. It includes basic authentication setup and error handling for API calls.

```java
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.util.*;
public class Demos {
    public static void google_shopping_html_tasks_get_by_task_id() throws JSONException, IOException, URISyntaxException {
        URI url = new URI("https://api.dataforseo.com/v2/merchant_google_shopping_html_tasks_get");
        HttpClient client;
        client = HttpClientBuilder.create().build();
        HttpGet get = new HttpGet(url);
        //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
        String basicAuth = Base64.getEncoder().encodeToString(("login:password").getBytes("UTF-8"));
        get.setHeader("Content-type", "application/json");
        get.setHeader("Authorization", "Basic " + basicAuth);
        HttpResponse completedTasksResponse = client.execute(get);
        JSONObject completedTasksObj = new JSONObject(EntityUtils.toString(completedTasksResponse.getEntity()));
        if (completedTasksObj.get("status") == "error") {
            JSONObject errorObj = completedTasksObj.getJSONObject("error");
            System.out.println("error. Code: " + errorObj.get("code") + " Message: " + errorObj.get("message"));

```

--------------------------------

### Example API Call (Java)

Source: https://docs.dataforseo.com/v2/auth_java=

An example demonstrating how to make a basic GET request to the DataForSEO API using Java, including authentication.

```APIDOC
## Example API Call (Java)

### Description
This example demonstrates a simple GET request to the DataForSEO API using Java, including setting up Basic Authentication.

### Method
GET

### Endpoint
`https://api.dataforseo.com/` (This is a general example; specific endpoints will vary)

### Parameters
N/A for this general example, specific endpoints will have their own parameters.

### Request Body
N/A for this general example.

### Request Example
```java
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;
import java.net.URI;
import java.util.Base64;

public class DataForSEOExample {
    public static void main(String[] args) {
        try {
            URI url = new URI("https://api.dataforseo.com/"); // Replace with a specific endpoint
            HttpClient client = HttpClientBuilder.create().build();
            
            // Replace 'login' and 'password' with your actual credentials
            String credentials = "login:password";
            String basicAuth = Base64.getEncoder().encodeToString(credentials.getBytes("UTF-8"));
            
            HttpGet request = new HttpGet(url.toString());
            request.setHeader("Authorization", "Basic " + basicAuth);
            request.setHeader("Content-Type", "application/json");

            HttpResponse response = client.execute(request);
            String responseBody = EntityUtils.toString(response.getEntity());
            
            System.out.println("Status Code: " + response.getStatusLine().getStatusCode());
            System.out.println("Response Body: " + responseBody);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### Response
#### Success Response (200)
- **responseBody** (string) - The JSON response from the API.

#### Response Example
```json
{
  "status": "success",
  "data": { ... }
}
```

#### Error Response
- **status** (string) - "error"
- **error_message** (string) - Description of the error.

#### Error Response Example
```json
{
  "status": "error",
  "error_message": "Invalid credentials"
}
```
```

--------------------------------

### Fetch Lighthouse Tasks Ready (Python)

Source: https://docs.dataforseo.com/v3/on_page/lighthouse/tasks_ready_php=

This Python script uses a provided `RestClient` class to fetch lighthouse tasks from the DataForSEO API. It requires downloading the `python_Client.zip` example file. The script initializes the client with login credentials and then calls the `get` method to retrieve task status. Ensure you replace 'login' and 'password' with your actual credentials.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# using this method you can get a list of completed tasks
# GET /v3/on_page/lighthouse/tasks_ready
response = client.get("/v3/on_page/lighthouse/tasks_ready")
```

--------------------------------

### C#: Post Task for Google Extended Reviews with Options

Source: https://docs.dataforseo.com/v3/business_data/google/extended_reviews/task_post

This C# example demonstrates how to post tasks to the DataForSEO API for extended Google reviews. It shows how to configure the HttpClient with authentication and includes examples for setting task parameters like location, language, keyword, depth, priority, and pingback/postback URLs.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task business_data_google_extended_reviews_task_post()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            // simple way to set a task

            postData.Add(new

            {

                location_name = "London,England,United Kingdom",

                language_name = "English",

                keyword = "hedonism wines"

            });

            // after a task is completed, we will send a GET request to the address you specify

            // instead of $id and $tag, you will receive actual values that are relevant to this task

            postData.Add(new

            {

                location_name = "London,England,United Kingdom",

                language_name = "English",

                keyword = "hedonism wines",

                depth = 40,

                priority = 2,

                tag = "some_string_123",

                pingback_url = "https://your-server.com/pingscript?id=$id&tag=$tag"

            });

            // after a task is completed, we will send a GET request to the address you specify

            // instead of $id and $tag you will receive actual values that are relevant to this task

            postData.Add(new

            {

                location_name = "London,England,United Kingdom",

                language_name = "English",

                keyword = "hedonism wines",

                postback_url = "https://your-server.com/postbackscript"

            });

            // POST /v3/business_data/google/extended_reviews/task_post

            var taskPostResponse = await httpClient.PostAsync("/v3/business_data/google/extended_reviews/task_post", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get DataForSEO Labs Status using C#

Source: https://docs.dataforseo.com/v3/dataforseo_labs/status

This C# example shows how to retrieve the status of the DataForSEO Labs API using HttpClient. It includes authentication setup, making an asynchronous GET request, deserializing the JSON response, and handling success or error conditions. Replace 'login' and 'password' with your API credentials.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_status()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of endpoints

            // GET /v3/dataforseo_labs/status

            var response = await httpClient.GetAsync("/v3/dataforseo_labs/status");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Fetch Languages for Google Categories (Node.js)

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/categories_for_keywords/languages

This Node.js example uses the 'axios' library to send a GET request to the DataForSEO API for supported languages. It handles successful responses by logging the language data and catches errors during the request. Remember to install axios (`npm install axios`).

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/dataforseo_labs/google/categories_for_keywords/languages',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Example of Pingback URL Configuration

Source: https://docs.dataforseo.com/v3/serp/yahoo/organic/task_post

Shows how to configure a `pingback_url` to receive a GET request notification when a task is completed. Similar to postback URLs, it supports dynamic variables like `$id` and `$tag`.

```Bash
http://your-server.com/pingscript?id=$id
http://your-server.com/pingscript?id=$id&tag=$tag
```

--------------------------------

### Get Keywords for Keywords Data (C#)

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords/live

This C# example demonstrates how to make a POST request to the '/v3/keywords_data/google_ads/keywords_for_keywords/live' endpoint using HttpClient. It includes setting up authentication, serializing request data to JSON, sending the request, and deserializing the JSON response. It also handles response status codes similarly to the Python example.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_keywords_for_keywords_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                location_name = "United States",

                keywords = ["phone", "cellphone"]

            });

            // POST /v3/keywords_data/google_ads/keywords_for_keywords/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/keywords_data/google_ads/keywords_for_keywords/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic&gt(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Fetch Lighthouse Tasks Ready (Bash)

Source: https://docs.dataforseo.com/v3/on_page/lighthouse/tasks_ready_php=

This Bash script demonstrates how to fetch a list of ready lighthouse tasks from the DataForSEO API. It uses `curl` for making the HTTP GET request and Base64 encoding for basic authentication. Ensure you replace 'login' and 'password' with your actual API credentials.

```bash
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"

curl --location --request GET "https://api.dataforseo.com/v3/on_page/lighthouse/tasks_ready" \
--header "Authorization: Basic ${cred}" \
--header "Content-Type: application/json" \
--data-raw ""
```

--------------------------------

### Fetch Lighthouse Tasks Ready (Node.js)

Source: https://docs.dataforseo.com/v3/on_page/lighthouse/tasks_ready_php=

This Node.js example uses the `axios` library to make a GET request to the DataForSEO API for fetching lighthouse tasks. It demonstrates setting up the request with authentication (username and password) and headers. The response contains task results, which are logged to the console. Error handling for the request is also included.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/on_page/lighthouse/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch Ready App List Tasks using PHP

Source: https://docs.dataforseo.com/v3/app_data/google/app_list/tasks_ready

This PHP code example shows how to fetch a list of ready app data tasks from the DataForSEO API using the provided RestClient. It handles potential exceptions and prints the API response. Make sure to replace placeholder credentials with your actual login and password.

```php
<?php

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');



try {

   // using this method you can get a list of completed tasks

   // GET /v3/app_data/google/app_list/tasks_ready

   $result = $client->get('/v3/app_data/google/app_list/tasks_ready');

   print_r($result);

   // do something with result

} catch (RestClientException $e) {

   echo "\n";

   print "HTTP code: {$e->getHttpCode()}\n";

   print "Error code: {$e->getCode()}\n";

   print "Message: {$e->getMessage()}\n";

   print  $e->getTraceAsString();

   echo "\n";

}

$client = null;

?>
```

--------------------------------

### Check DataForSEO API Task Readiness (C#)

Source: https://docs.dataforseo.com/v3/keywords_data/bing/keyword_performance/tasks_ready_php=

This C# example shows how to asynchronously check if tasks are ready for the DataForSEO Keywords Data API. It includes setting up an HttpClient with authentication, making a GET request, deserializing the JSON response, and handling success or error statuses.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/keywords_data/bing/keyword_performance/tasks_ready

            // in addition to 'keyword_performance' you can also set other parameters

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/keywords_data/bing/keyword_performance/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### GET Request Example for Merchant Google Shopping Tasks

Source: https://docs.dataforseo.com/v2/merchant_python=

This example demonstrates a GET request to the `v2/merchant_google_shopping_tasks_get` endpoint. This endpoint is used to retrieve a list of completed tasks for which results have not yet been collected. The response will be a JSON object containing task details.

```http
GET https://api.dataforseo.com/v2/merchant_google_shopping_tasks_get
```

--------------------------------

### C#: Fetch Ready AI Optimization Tasks

Source: https://docs.dataforseo.com/v3/ai_optimization/gemini/llm_responses/tasks_ready

This C# example demonstrates fetching AI optimization tasks using `HttpClient`. It sets up the base address and authorization headers, then makes a GET request to the tasks ready endpoint. The response is deserialized using Newtonsoft.Json.

```csharp
using System;

using System.Linq;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Collections.Generic;

using System.Threading.Tasks;

using Newtonsoft.Json;

namespace DataForSeoSdk;



public class AiOptimization

{



    private static readonly HttpClient _httpClient;

    

    static AiOptimization()

    {

        _httpClient = new HttpClient

        {

            BaseAddress = new Uri("https://api.dataforseo.com/")

        };

        _httpClient.DefaultRequestHeaders.Authorization =

            new AuthenticationHeaderValue("Basic", ApiConfig.Base64Auth);

    }



    /// <summary>

    /// Method: GET

    /// Endpoint: https://api.dataforseo.com/v3/ai_optimization/gemini/llm_responses/tasks_ready

    /// </summary>

    /// <see href="https://docs.dataforseo.com/v3/ai_optimization/gemini/llm_responses/tasks_ready"/>

    

    public static async Task ChatGPTLlmResponsesTaskGet()

    {

        // #1 - using this method you can get a list of completed tasks

        using var response = await _httpClient.GetAsync("/v3/ai_optimization/gemini/llm_responses/tasks_ready");

        var tasksInfo = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

        var tasksResponses = new List<object>();

        // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

        if (tasksInfo.status_code == 20000)

        {

            if (tasksInfo.tasks != null)

            {

                foreach (var tasks in tasksInfo.tasks)

                {

                    if (tasks.result != null)

                    {

                        foreach (var task in tasks.result)

                        {

                            string taskEndpoint = null;                            

                            // #2 - using this method you can get results of each completed task

                            if (task.endpoint != null)

                                taskEndpoint = (string)task.endpoint;

                            

                            if (taskEndpoint != null)

                            {

                                using var taskGetResponse = await _httpClient.GetAsync(taskEndpoint);

                                var taskResultObj = JsonConvert.DeserializeObject<dynamic>(await taskGetResponse.Content.ReadAsStringAsync());

                                if (taskResultObj.tasks != null)

```

--------------------------------

### Get Ad Traffic by Keywords (Python)

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/ad_traffic_by_keywords/tasks_ready

This Python example uses a RestClient class to interact with the DataForSEO API. It shows how to initialize the client with your login and password, and then make a GET request to the 'tasks_ready' endpoint for retrieving ad traffic by keywords. Ensure the 'client.py' file is available in your project.

```python
from random import Random

from client import RestClient

# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip



client = RestClient("login", "password")

# using this method you can get a list of completed tasks

# GET /v3/keywords_data/google_ads/ad_traffic_by_keywords/tasks_ready

# in addition to 'ad_traffic_by_keywords' you can also set other parameters

# the full list of possible parameters is available in documentation

response = client.get("/v3/keywords_data/google_ads/ad_traffic_by_keywords/tasks_ready")
```

--------------------------------

### JavaScript Axios Example

Source: https://docs.dataforseo.com/v3/keywords_data/google/search_volume/task_get

Example using Axios in JavaScript to make a GET request to the DataForSEO API to retrieve task results.

```APIDOC
## JavaScript Axios Example

### Description
This example shows how to use the Axios library in JavaScript to fetch search volume data for a given task ID from the DataForSEO API.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/keywords_data/google/search_volume/task_get/{task_id}

### Parameters
#### Path Parameters
- **task_id** (string) - Required - The ID of the task to retrieve results for.

#### Authorization
- **username** (string) - Your DataForSEO API login.
- **password** (string) - Your DataForSEO API password.

### Request Example
```javascript
const task_id = '02231934-2604-0066-2000-570459f04879';

const axios = require('axios');
axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/keywords_data/google/search_volume/task_get/' + task_id,
    auth: {
        username: 'login',
        password: 'password'
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response['data']['tasks'];
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

### Response
#### Success Response (200)
- **tasks** (array) - An array containing the task results.

#### Response Example
```json
[
  {
    "result": [
      {
        "keyword": "example keyword",
        "search_volume": 1000
      }
    ]
  }
]
```
```

--------------------------------

### Fetch Amazon Product Competitors Live Data (C#)

Source: https://docs.dataforseo.com/v3/dataforseo_labs/amazon/product_competitors/live_bash=

This C# example demonstrates how to fetch live Amazon product competitor data using the DataForSEO API. It uses HttpClient to make a POST request to the '/v3/dataforseo_labs/amazon/product_competitors/live' endpoint with specified parameters like ASIN, location, and language. It handles authentication using Basic HTTP authentication and deserializes the JSON response, checking for a success status code.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_amazon_product_competitors_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))

                }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                asin = "019005476X",

                location_name = "United States",

                language_name = "English"

            });

            // POST /v3/dataforseo_labs/amazon/product_competitors/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/amazon/product_competitors/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Google Local Finder Tasks Ready using Python

Source: https://docs.dataforseo.com/v3/serp/google/local_finder/task_get/advanced

This Python example shows how to fetch a list of completed tasks for Google Local Finder using the provided RestClient class. It demonstrates how to initialize the client with credentials and make a GET request to the tasks_ready endpoint.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# 1 - using this method you can get a list of completed tasks
# GET /v3/serp/google/local_finder/tasks_ready
# in addition to 'google' and 'local_finder' you can also set other search engine and type parameters
# the full list of possible parameters is available in documentation
response = client.get("/v3/serp/google/local_finder/tasks_ready")
```

--------------------------------

### Fetch Business Listing Categories with C#

Source: https://docs.dataforseo.com/v3/business_data/business_listings/categories

This C# example shows how to make a GET request to the /v3/business_data/business_listings/categories endpoint using HttpClient. It includes authentication setup and deserialization of the JSON response, handling both success and error cases.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_categories()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of categories

            // GET /v3/dbusiness_data/business_listings/categories

            var response = await httpClient.GetAsync("/v3/business_data/business_listings/categories");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Example of Postback URL Configuration

Source: https://docs.dataforseo.com/v3/serp/yahoo/organic/task_post

Illustrates how to set up a `postback_url` to receive task results via a POST request upon completion. The URL can include variables like `$id` and `$tag` for dynamic data inclusion.

```Bash
http://your-server.com/postbackscript?id=$id
http://your-server.com/postbackscript?id=$id&tag=$tag
```

--------------------------------

### Get Lighthouse Versions using PHP

Source: https://docs.dataforseo.com/v3/on_page/lighthouse/versions

This PHP example demonstrates how to use the provided RestClient class to fetch Lighthouse versions. It includes error handling for API requests and initializes the client with API credentials.

```php
<?php

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {
    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
    $client = new RestClient($api_url, null, 'login', 'password');
} catch (RestClientException $e) {
    echo "n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "n";
    exit();
}

try {
    // using this method you can get a list of available versions
    // GET /v3/on_page/lighthouse/versions
    $result = $client->get('/v3/on_page/lighthouse/versions');
    print_r($result);
    // do something with result
} catch (RestClientException $e) {
    echo "n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "n";
}

$client = null;

?>
```

--------------------------------

### GET /v3/keywords_data/bing/audience_estimation/tasks_ready (Python)

Source: https://docs.dataforseo.com/v3/keywords_data/bing/audience_estimation/tasks_ready

Example using Python RestClient to get a list of completed tasks for Bing audience estimation.

```APIDOC
## GET /v3/keywords_data/bing/audience_estimation/tasks_ready (Python)

### Description
This Python code snippet utilizes the RestClient to retrieve completed tasks for Bing audience estimation. It requires authentication with username and password.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/keywords_data/bing/audience_estimation/tasks_ready

### Parameters

#### Path Parameters
None

#### Query Parameters
None

#### Request Body
This endpoint does not require a request body.

### Request Example
```python
from random import Random
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip


client = RestClient("login", "password")
# using this method you can get a list of completed tasks
# GET /v3/keywords_data/bing/audience_estimation/tasks_ready
response = client.get("/v3/keywords_data/bing/audience_estimation/tasks_ready")

print(response)
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks.
  - **id** (string) - The ID of the task.
  - **result** (object) - The result of the task.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "result": {
        "some_data": "example"
      }
    }
  ]
}
```
```

--------------------------------

### GET /v3/keywords_data/bing/audience_estimation/tasks_ready (Node.js)

Source: https://docs.dataforseo.com/v3/keywords_data/bing/audience_estimation/tasks_ready

Example using Axios in Node.js to get a list of completed tasks for Bing audience estimation.

```APIDOC
## GET /v3/keywords_data/bing/audience_estimation/tasks_ready (Node.js)

### Description
This Node.js code snippet uses the Axios library to make a GET request to the Bing audience estimation tasks ready endpoint. It includes basic authentication and response handling.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/keywords_data/bing/audience_estimation/tasks_ready

### Parameters

#### Path Parameters
None

#### Query Parameters
None

#### Request Body
This endpoint does not require a request body.

### Request Example
```javascript
const axios = require('axios');

axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/keywords_data/bing/audience_estimation/tasks_ready',
    auth: {
        username: 'login',
        password: 'password'
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response['data']['tasks'][0]['result'];
    // Result data
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks.
  - **id** (string) - The ID of the task.
  - **result** (object) - The result of the task.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "result": {
        "some_data": "example"
      }
    }
  ]
}
```
```

--------------------------------

### JavaScript (Node.js): Authenticate and GET Local Finder Tasks

Source: https://docs.dataforseo.com/v3/serp/google/local_finder/tasks_fixed

This JavaScript example uses the 'axios' library to interact with the Dataforseo API. It demonstrates setting up authentication with username and password and making a GET request to retrieve data for the Google Local Finder tasks.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/google/local_finder/tasks_fixed',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### GET /v3/keywords_data/bing/audience_estimation/tasks_ready (PHP)

Source: https://docs.dataforseo.com/v3/keywords_data/bing/audience_estimation/tasks_ready

Example using PHP RestClient to get a list of completed tasks for Bing audience estimation.

```APIDOC
## GET /v3/keywords_data/bing/audience_estimation/tasks_ready (PHP)

### Description
This PHP code snippet demonstrates how to use the RestClient to fetch completed tasks for Bing audience estimation. It includes error handling for API requests.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/keywords_data/bing/audience_estimation/tasks_ready

### Parameters

#### Path Parameters
None

#### Query Parameters
None

#### Request Body
This endpoint does not require a request body.

### Request Example
```php
<?php

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {
    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
    $client = new RestClient($api_url, null, 'login', 'password');
} catch (RestClientException $e) {
    echo "n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "n";
    exit();
}

try {
    // using this method you can get a list of completed tasks
    // GET /v3/keywords_data/bing/audience_estimation/tasks_ready
    $result = $client->get('/v3/keywords_data/bing/audience_estimation/tasks_ready');
    print_r($result);
} catch (RestClientException $e) {
    echo "n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "n";
}

$client = null;

?>
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks.
  - **id** (string) - The ID of the task.
  - **result** (object) - The result of the task.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "result": {
        "some_data": "example"
      }
    }
  ]
}
```
```

--------------------------------

### GET /v3/business_data/tripadvisor/search/tasks_ready (JavaScript/axios)

Source: https://docs.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready

This JavaScript example uses the axios library to make a GET request for completed TripAdvisor search tasks, including authentication and response handling.

```APIDOC
## GET /v3/business_data/tripadvisor/search/tasks_ready (JavaScript/axios)

### Description
Retrieves a list of completed tasks for TripAdvisor searches using the axios library in JavaScript.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```javascript
const axios = require('axios');

axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready',
    auth: {
        username: 'your_login',
        password: 'your_password'
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response['data']['tasks'][0]['result'];
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "status_code": 200,
      "status_message": "Success",
      "time_taken": "0.123s",
      "result_count": 1,
      "path": [
        "business_data",
        "tripadvisor",
        "search"
      ],
      "data": [],
      "info": {
        "count": 1,
        "time_taken": "0.123s"
      },
      "cost": 0.001
    }
  ]
}
```
```

--------------------------------

### Python Client - GET /v3/keywords_data/bing/keyword_suggestions_for_url/tasks_ready

Source: https://docs.dataforseo.com/v3/keywords_data/bing/keyword_suggestions_for_url/tasks_ready

Example of using the Python client to get a list of completed tasks for keyword suggestions for a URL on Bing. Requires specifying login and password for authentication.

```APIDOC
## GET /v3/keywords_data/bing/keyword_suggestions_for_url/tasks_ready (Python Client)

### Description
Example of using the Python client to get a list of completed tasks for keyword suggestions for a URL on Bing. Requires specifying login and password for authentication.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/keywords_data/bing/keyword_suggestions_for_url/tasks_ready

### Parameters

#### Query Parameters
- **None** (This endpoint does not specify query parameters in the provided examples).

### Request Example (Python)
```python
from random import Random
from client import RestClient

# Assuming python_Client.zip has been downloaded and RestClient is available
client = RestClient("login", "password")

# Using this method you can get a list of completed tasks
# GET /v3/keywords_data/bing/keyword_suggestions_for_url/tasks_ready
response = client.get("/v3/keywords_data/bing/keyword_suggestions_for_url/tasks_ready")

# The actual response handling and printing is omitted in the provided snippet
# but would typically involve checking response status and parsing the data.
# For example:
# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print(f"Error: {response.status_code}")
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks.
  - **id** (string) - The ID of the task.
  - **status_code** (integer) - The status code of the task.
  - **status_message** (string) - The status message for the task.
  - **cost** (number) - The cost associated with the task.
  - **result_url** (string) - The URL to retrieve the task results.
  - **created_at** (string) - The timestamp when the task was created.
  - **updated_at** (string) - The timestamp when the task was last updated.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "example_task_id_3",
      "status_code": 200,
      "status_message": "Task completed successfully.",
      "cost": 0.002,
      "result_url": "https://api.dataforseo.com/v3/keywords_data/bing/keyword_suggestions_for_url/results/example_task_id_3",
      "created_at": "2024-01-01 11:30:00",
      "updated_at": "2024-01-01 11:35:00"
    }
  ]
}
```
```

--------------------------------

### Get Google Keyword Overview Live Data using Python

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live

This Python example shows how to use the provided RestClient class to fetch live keyword overview data from Google. It requires importing the RestClient, initializing it with credentials, and then making a POST request with the keyword details. The response from the API is then printed.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    keywords=[
        "iphone"
    ],
    location_name="United States",
    language_name="English"
)
# POST /v3/dataforseo_labs/google/keyword_overview/live
response = client.post("/v3/dataforseo_labs/google/keyword_overview/live", post_data)
```

--------------------------------

### Authenticate and Get Google Hotel Info Tasks Ready (Python)

Source: https://docs.dataforseo.com/v3/business_data/google/hotel_info/tasks_ready

This Python example utilizes a `RestClient` class to authenticate with the DataForSEO API using provided login and password credentials. It then makes a GET request to the `/v3/business_data/google/hotel_info/tasks_ready` endpoint.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# using this method you can get a list of completed tasks
# GET /v3/business_data/google/hotel_info/tasks_ready
response = client.get("/v3/business_data/google/hotel_info/tasks_ready")
```

--------------------------------

### Post SERP Task with Priority and Pingback (C#)

Source: https://docs.dataforseo.com/v3/serp/bing/organic/task_post

This C# example demonstrates posting a SERP task with advanced options. It includes setting the language by name, location by name, a keyword, a task priority, and a pingback URL with dynamic parameters for ID and tag. This allows for faster task completion and asynchronous notification upon completion.

```csharp
var httpClient = new HttpClient
{
    BaseAddress = new Uri("https://api.dataforseo.com/"),
    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
    DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
};

var postData = new List<object>();

// example #2 - a way to set a task with additional parameters
// high priority allows us to complete a task faster, but you will be charged more credits.
// after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.
postData.Add(new
{
    language_name = "English",
    location_name = "United States",
    keyword = "albert einstein",
    priority = 2,
    tag = "some_string_123",
    pingback_url = "https://your-server.com/pingscript?id=$id&tag=$tag"
});

// POST /v3/serp/bing/organic/task_post
// in addition to 'bing' and 'organic' you can also set other search engine and type parameters
// the full list of possible parameters is available in documentation
var taskPostResponse = await httpClient.PostAsync("/v3/serp/bing/organic/task_post", new StringContent(JsonConvert.SerializeObject(postData)));
var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

// you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if (result.status_code == 20000)
{
    // do something with result
    Console.WriteLine(result);
}
else
    Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

```

--------------------------------

### Retrieve Product URL using ad_aclk (PHP)

Source: https://docs.dataforseo.com/v2/merchant_python=

Example of how to use the merchant_google_shopping_shops_ad_url endpoint in PHP to get a product URL. It demonstrates making the GET request and processing the JSON response.

```php
<?php

// Example usage
$ad_aclk = "YOUR_AD_ACLK_PARAMETER";
$url = "https://api.dataforseo.com/v2/merchant_google_shopping_shops_ad_url/".$ad_aclk;

$ch = curl_init();
c_setopt($ch, CURLOPT_URL, $url);
c_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$response = curl_exec($ch);
c_close($ch);

$data = json_decode($response, true);

if (isset($data['results']) && !empty($data['results'])) {
    foreach ($data['results'] as $result) {
        if ($result['status'] === 'ok') {
            echo "Product URL: " . $result['ai_url'] . "\n";
        } else {
            echo "Error: " . $result['error'][0]['message'] . "\n";
        }
    }
} else {
    echo "No results found or an error occurred.";
}

?>
```

--------------------------------

### C#: Fetch Live Referring Domains with Filters

Source: https://docs.dataforseo.com/v3/backlinks/referring_domains/live

This C# example demonstrates how to call the DataForSeo API for live referring domains using HttpClient. It sets up authorization headers, constructs the POST data with target, filters, and ordering parameters, sends the request, and deserializes the JSON response. It then checks the status code to determine if the operation was successful or if an error occurred.

```csharp
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

// ... inside a static method like backlinks_referring_domains_live ...

var httpClient = new HttpClient
{
    BaseAddress = new Uri("https://api.dataforseo.com/"),
    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
    DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
};

var postData = new List<object>();
postData.Add(new
{
    target = "backlinko.com",
    exclude_internal_backlinks = true,
    backlinks_filters = new object[]
    {
        new object[] { "dofollow", "=", true }
    },
    filters = new object[]
    {
        new object[] { "backlinks", ">", 100 }
    },
    order_by = new object[] { "rank,desc" },
    limit = 5
});

// POST /v3/backlinks/referring_domains/live
var taskPostResponse = await httpClient.PostAsync("/v3/backlinks/referring_domains/live", new StringContent(JsonConvert.SerializeObject(postData)));
var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

if (result.status_code == 20000)
{
    Console.WriteLine(result);
}
else
    Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

```

--------------------------------

### Python: Get list of completed tasks

Source: https://docs.dataforseo.com/v3/serp/seznam/organic/task_get/advanced

Example using the RestClient in Python to get a list of completed organic search tasks.

```APIDOC
## Python Example

### Description
This Python script demonstrates how to use the `RestClient` class to fetch a list of completed organic search tasks for Seznam.

### Method
GET

### Endpoint
`/v3/serp/seznam/organic/tasks_ready`

### Parameters
(See general API documentation for parameter details)

### Request Example
```python
from client import RestClient

# Replace 'login' and 'password' with your actual credentials
client = RestClient("your_login", "your_password")

# Get a list of completed tasks
try:
    response = client.get("/v3/serp/seznam/organic/tasks_ready")
    # Process the response
    if response and response['status_code'] == 20000:
        print("Successfully retrieved tasks:")
        # You can further process response['tasks'] here
        # print(response['tasks'])
    else:
        print("Failed to retrieve tasks. Status code:", response.get('status_code'))
        print("Error message:", response.get('msg'))
except Exception as e:
    print(f"An error occurred: {e}")

```
```

--------------------------------

### Configure POST Postback for Task Completion (Python)

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/task_post_php=

This snippet demonstrates setting up data for a POST request upon task completion. It includes location name, keywords, and a postback URL. Unlike the GET pingback, this example uses a direct postback URL without explicit placeholders.

```python
post_data[len(post_data)] = dict(

    location_name="United States",

    keywords=[

        "buy laptop",

        "cheap laptops for sale",

        "purchase laptop"

    ],

    postback_url="https://your-server.com/postbackscript"

)
```

--------------------------------

### Get User Info with C# HttpClient

Source: https://docs.dataforseo.com/v2/cmn_csharp=

Fetches user data using HttpClient in C#. This example utilizes Newtonsoft.Json for JSON deserialization and basic authentication. It prints user details or error information.

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task cmn_user()
        {
            var httpClient = new HttpClient {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };
            var response = await httpClient.GetAsync("v2/cmn_user");
            var obj = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());
            if (obj.status == "error")
                Console.WriteLine($"error. Code: {obj.error.code} Message: {obj.error.message}");
            else

```

--------------------------------

### Fetch Google Hotel Info Live Data (C#)

Source: https://docs.dataforseo.com/v3/business_data/google/hotel_info/live/html

This C# example demonstrates how to fetch live hotel information from Google using the DataForSeo API. It utilizes `HttpClient` to make a POST request to the '/v3/business_data/google/hotel_info/live/html' endpoint. The example shows how to set authentication headers, construct the request body with different location and identifier formats, and deserialize the JSON response. Error handling is included based on the 'status_code'.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task business_data_info_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            // example #1 - a simple way to set a task

            // this way requires you to specify a location, a language of search, and a hotel_identifier.

            postData.Add(new

            {

                language_code = "en",

                location_code = 1023191,

                hotel_identifier = "ChYIq6SB--i6p6cpGgovbS8wN2s5ODZfEAE"

            });

            // example #2 - a way to set a task with additional parameters

            postData.Add(new

            {

                language_name = "English",

                location_name = "New York,New York,United States",

                hotel_identifier = "ChYIq6SB--i6p6cpGgovbS8wN2s5ODZfEAE"

            });

            // POST /v3/business_data/google/hotel_info/live/html

            var taskPostResponse = await httpClient.PostAsync("/v3/business_data/google/hotel_info/live/html", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Authenticate and Get Product Info (Bash)

Source: https://docs.dataforseo.com/v3/merchant/google/product_info/tasks_ready

This Bash script shows how to authenticate with the Dataforseo API using basic authentication and retrieve ready tasks for Google product information. It constructs a base64 encoded credential string and makes a GET request to the /v3/merchant/google/product_info/tasks_ready endpoint.

```bash
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access 

login="login" 

password="password" 

cred="$(printf ${login}:${password} | base64)" 

curl --location --request GET "https://api.dataforseo.com/v3/merchant/google/product_info/tasks_ready" 

--header "Authorization: Basic ${cred}"  

--header "Content-Type: application/json" 

--data-raw ""
```

--------------------------------

### Submit Google Shopping Task using IDs (PHP)

Source: https://docs.dataforseo.com/v2/merchant

This example demonstrates the fastest method for setting a task by providing pre-defined IDs: 'se_id', 'loc_id', and 'key_id'. These IDs can be obtained from the DataForSEO documentation. This method is recommended for performance-critical applications.

```php
// example #3 - the fastest one. All parameters should be set in our internal format.
// Actual and fresh list can be found here: "se_id": https://api.dataforseo.com/v2/cmn_se ,
// "loc_id": https://api.dataforseo.com/v2/cmn_locations
// You must choose a search engine with the word "shopping" included into the "se_name" field
$my_unq_id = mt_rand(0,30000000); //your unique ID. we will return it with all results. you can set your database ID, string, etc.
$post_array[$my_unq_id] = array(
"priority" => 1,
"se_id" => 2933,
"loc_id" => 1006886,
"key_id" => 68415
);
```

--------------------------------

### Get AdWords Status using C#

Source: https://docs.dataforseo.com/v2/cmn_python=

This C# example illustrates fetching AdWords status via the DataForSeo API. It employs HttpClient for making the GET request and Newtonsoft.Json for deserializing the JSON response. Ensure your API credentials ('login', 'password') are correctly provided.

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task cmn_adwords_status()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))
            };
            var response = await httpClient.GetAsync("v2/cmn_adwords_status");
            var obj = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());
            if (obj.status == "error")

```

--------------------------------

### App Data API - Python Client Example

Source: https://docs.dataforseo.com/v3/app_data/apple/app_searches/task_get/advanced

Example of how to use the Python client to fetch advanced app search task results. This snippet demonstrates authenticating and making a GET request to retrieve task data.

```APIDOC
## App Data API - Python Client Example

### Description
Example of how to use the Python client to fetch advanced app search task results. This snippet demonstrates authenticating and making a GET request to retrieve task data.

### Method
GET

### Endpoint
/v3/app_data/apple/app_searches/task_get/advanced/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier of the task for which to retrieve results.

### Request Example
```python
from client import RestClient
client = RestClient("login", "password")
id = "06141103-2692-0309-1000-980b778b6d25"
response = client.get("/v3/app_data/apple/app_searches/task_get/advanced/" + id)
print(response)
```

### Response
#### Success Response (200)
- **tasks** (array) - An array containing the results for the specified task ID.

#### Response Example
```json
[
  {
    "rating_max": 5,
    "is_free": false,
    "price": {
      "current": 4.99,
      "regular": 4.99,
      "max_value": 4.99,
      "currency": "USD"
    },
    "is_price_range": false,
    "displayed_price": "$4.99"
  }
]
```
```

--------------------------------

### Post Google Shopping Shops Tasks - Java (Setup)

Source: https://docs.dataforseo.com/v2/merchant_java=

This Java code snippet provides the setup for posting tasks to the DataforSEO v2 merchant_google_shopping_shops_tasks_
post endpoint. It includes necessary imports and the method signature for initiating the task posting process. The actual HTTP request and response handling logic would follow this setup.

```java
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.util.*;
public class Demos {
    public static void merchant_google_shopping_
_shops_tasks_post() throws JSONException, IOException, URISyntaxException {

```

--------------------------------

### Get Google Merchant Languages List (C#)

Source: https://docs.dataforseo.com/v3/merchant/google/languages

This C# example demonstrates how to call the DataForSEO API endpoint for retrieving a list of Google Merchant languages. It uses HttpClient for making the request and Newtonsoft.Json for deserializing the JSON response. The code includes authentication setup and error handling based on the 'status_code'.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task merchant_google_languages()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of languages

            // GET /v3/merchant/google/languages

            var response = await httpClient.GetAsync("/v3/merchant/google/languages");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### GET /v3/business_data/tripadvisor/search/tasks_ready (Python)

Source: https://docs.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready

This Python example demonstrates how to use the RestClient to retrieve completed TripAdvisor search tasks.

```APIDOC
## GET /v3/business_data/tripadvisor/search/tasks_ready (Python)

### Description
Retrieves a list of completed tasks for TripAdvisor searches using the Python RestClient.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```python
from client import RestClient

client = RestClient("your_login", "your_password")

response = client.get("/v3/business_data/tripadvisor/search/tasks_ready")

print(response)
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "status_code": 200,
      "status_message": "Success",
      "time_taken": "0.123s",
      "result_count": 1,
      "path": [
        "business_data",
        "tripadvisor",
        "search"
      ],
      "data": [],
      "info": {
        "count": 1,
        "time_taken": "0.123s"
      },
      "cost": 0.001
    }
  ]
}
```
```

--------------------------------

### Make SERP Live Regular API Call (C#)

Source: https://docs.dataforseo.com/v3/serp/google/organic/live/regular

This C# example demonstrates how to make a POST request to the /v3/serp/google/organic/live/regular endpoint using HttpClient and Newtonsoft.Json. It includes setting up the client, defining request data, sending the request, and deserializing the JSON response. It requires the System.Net.Http, System.Threading.Tasks, System.Collections.Generic, and Newtonsoft.Json namespaces.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_live_regular()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                //DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))

            };

            var postData = new List<object>();

            // You can set only one task at a time

            postData.Add(new

            {

                language_code = "en",

                location_code = 2840,

                keyword = "albert einstein"

            });

            // POST /v3/serp/google/organic/live/regular

            // in addition to 'google' and 'organic' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/serp/google/organic/live/regular", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Setting Task Priority and Location (Example)

Source: https://docs.dataforseo.com/v3/serp/google/organic/task_post

Demonstrates how to set task priority and specify location using location_name. This is useful for prioritizing urgent tasks and targeting specific geographical areas for search engine results.

```json
{
  "priority": 2,
  "location_name": "London,England,United Kingdom"
}
```

--------------------------------

### GET /v3/serp/google/ads_search/tasks_ready (Node.js)

Source: https://docs.dataforseo.com/v3/serp/google/ads_search/tasks_ready_php=

This Node.js example uses the axios library to make a GET request to retrieve completed tasks for Google Ads search. It includes basic error handling.

```APIDOC
## GET /v3/serp/google/ads_search/tasks_ready

### Description
Retrieves a list of completed tasks for Google Ads search using Node.js and axios.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/serp/google/ads_search/tasks_ready

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```javascript
const axios = require('axios');

axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/serp/google/ads_search/tasks_ready',
    auth: {
        username: 'login',
        password: 'password'
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response['data']['tasks'][0]['result'];
    // Result data
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

### Response
#### Success Response (200)
- **tasks** (array) - An array of completed tasks.
  - **id** (string) - The ID of the task.
  - **result** (object) - The result of the task.

#### Response Example
```json
{
    "tasks": [
        {
            "id": "01234567-89ab-cdef-0123-456789abcdef",
            "result": {
                "some_data": "example"
            }
        }
    ]
}
```
```

--------------------------------

### Node.js Example for Task Get Advanced

Source: https://docs.dataforseo.com/v3/serp/google/search_by_image/task_get/advanced

Demonstrates how to use Node.js with the Axios library to fetch advanced results for a 'search by image' task.

```APIDOC
## Node.js Example for Task Get Advanced

### Description
This example shows how to use the `axios` library in Node.js to make a GET request to the `/v3/serp/google/search_by_image/task_get/advanced/{id}` endpoint to retrieve detailed search results for an image search task.

### Method
GET

### Endpoint
/v3/serp/google/search_by_image/task_get/advanced/`{task_id}`

### Parameters
#### Path Parameters
- **task_id** (string) - Required - The ID of the task to retrieve results for.

#### Query Parameters
None

#### Request Body
None

### Request Example
```javascript
const axios = require('axios');

const task_id = 'YOUR_TASK_ID'; // Replace with your actual task ID

axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/serp/google/search_by_image/task_get/advanced/' + task_id,
    auth: {
        username: 'YOUR_LOGIN', // Replace with your login
        password: 'YOUR_PASSWORD' // Replace with your password
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response.data.tasks;
    console.log(result);
}).catch(function (error) {
    console.error(error);
});
```

### Response
#### Success Response (200 OK)
- **tasks** (array) - An array containing the results of the specified task.

#### Response Example
```json
[
  {
    "result": [
      {
        "se_type": "serp",
        "check_url": "...",
        "img_src": "...",
        "title": "...",
        "breadcrumb": "...",
        "displayed_link": "...",
        "link_to_page": "..."
      }
    ],
    "id": "YOUR_TASK_ID",
    "endpoint_advanced": "/v3/serp/google/search_by_image/task_get/advanced/YOUR_TASK_ID"
  }
]
```
```

--------------------------------

### C# Authentication and Usage Example

Source: https://docs.dataforseo.com/v2/auth_php=

This C# snippet illustrates how to set up an HttpClient for DataForSEO API authentication using Basic Authentication. Update 'login' and 'password' with your actual credentials.

```APIDOC
## C# API Authentication and Usage Example

### Description
This example demonstrates how to configure an `HttpClient` in C# for DataForSEO API authentication using Basic HTTP Authentication. Replace 'login' and 'password' with your API credentials.

### Method
N/A (Client-side script)

### Endpoint
`https://api.dataforseo.com/`

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task cmn_key_id()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),

                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };

            // do something
        }
    }
}
```

### Response
#### Success Response (200)
N/A (Client-side script, response depends on the 'do something' part)

#### Response Example
N/A
```

--------------------------------

### Fetch Backlinks Summary Live (C#)

Source: https://docs.dataforseo.com/v3/backlinks/summary/live

This C# example shows how to use the DataForSEO API to fetch backlink summary data for a given target domain. It utilizes `HttpClient` and `Newtonsoft.Json` to make a POST request to the `/v3/backlinks/summary/live` endpoint and process the JSON response. Authentication is handled via Basic HTTP authentication.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;

namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task backlinks_summary_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                target = "explodingtopics.com",

                internal_list_limit = 10,

                include_subdomains = true,

                backlinks_status_type = "all",

                backlinks_filters = new object[]

                {

                    new object[] { "dofollow", "=", true }

                }

            });

            // POST /v3/backlinks/summary/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/backlinks/summary/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Python Example for Tasks Ready

Source: https://docs.dataforseo.com/v3/serp/google/search_by_image/task_get/advanced

Provides a Python example using the RestClient to fetch a list of completed tasks.

```APIDOC
## Python Example for Tasks Ready

### Description
This Python script demonstrates how to use the `RestClient` to fetch a list of completed tasks for the Google 'search by image' endpoint. It shows the basic structure for authenticating and making a GET request to the `/v3/serp/google/search_by_image/tasks_ready` endpoint.

### Method
GET

### Endpoint
/v3/serp/google/search_by_image/tasks_ready

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
from client import RestClient

# Initialize the client with your login and password
client = RestClient("YOUR_LOGIN", "YOUR_PASSWORD")

# Make a GET request to retrieve a list of completed tasks
try:
    response = client.get("/v3/serp/google/search_by_image/tasks_ready")
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")

```

### Response
#### Success Response
- **tasks** (array) - A list of completed tasks. Each task object may contain an `id` and a `result` array with an `endpoint_advanced` field.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "02231934-2604-0066-2000-570459f04879",
      "result": [
        {
          "endpoint_advanced": "/v3/serp/google/search_by_image/task_get/advanced/02231934-2604-0066-2000-570459f04879"
        }
      ]
    }
  ],
  "status_code": 20000
}
```
```

--------------------------------

### API Request Examples (cURL, PHP, Node.js, Python, C#)

Source: https://docs.dataforseo.com/v3/serp/google/organic/task_get/advanced_php=

Examples of how to make API requests using different programming languages. Replace 'login' and 'password' with your actual API credentials.

```bash
curl -X POST \
  'https://api.dataforseo.com/v3/...' \
  -u 'login:password' \
  -H 'Content-Type: application/json' \
  -d '{"params":...}'
```

```php
<?php

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://api.dataforseo.com/v3/...');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    $headers = array();
    $headers[] = 'Content-Type: application/json';
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    $data = array(
        "params": ...
    );
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    $headers = array();
    $headers[] = 'Authorization: Basic ' . base64_encode('login:password');
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    $result = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    }
    curl_close($ch);
    
    print_r($result);

?>
```

```javascript
const https = require('https');

const options = {
  hostname: 'api.dataforseo.com',
  port: 443,
  path: '/v3/...',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + Buffer.from('login:password').toString('base64')
  }
};

const req = https.request(options, (res) => {
  res.on('data', (d) => {
    process.stdout.write(d);
  });
});

const data = JSON.stringify({
  "params": ...
});

req.write(data);
req.end();

req.on('error', (error) => {
  console.error(error);
});
```

```python
import requests

api_url = "https://api.dataforseo.com/v3/..."
login = "login"
password = "password"

params = {
    "params": ...
}

response = requests.post(api_url, auth=(login, password), json=params)

print(response.text)
```

```csharp
using System;
using System.Net.Http;
using System.Text;

public class DataForSeoApi
{
    public static void Main(string[] args)
    {
        string apiUrl = "https://api.dataforseo.com/v3/...";
        string login = "login";
        string password = "password";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes($"{login}:{password}")));
            
            string json = "{\"params\":...}";
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            
            HttpResponseMessage response = client.PostAsync(apiUrl, content).Result;
            string responseBody = response.Content.ReadAsStringAsync().Result;
            
            Console.WriteLine(responseBody);
        }
    }
}
```

--------------------------------

### Fetch Google Ads Search Volume Live - C#

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/live

This C# example shows how to use HttpClient to call the DataForSEO API for live Google Ads search volume data. It demonstrates setting up the HttpClient with authentication, preparing the POST data including keywords and location, sending the request asynchronously, deserializing the JSON response, and handling success or error statuses.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_search_volume_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                location_code = 2840,

                keywords = new[]

                {

                    "buy laptop",

                    "cheap laptops for sale",

                    "purchase laptop"

                },

                date_from: "2021-08-01",

                search_partners: true 

            });

            // POST /v3/keywords_data/google_ads/search_volume/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/keywords_data/google_ads/search_volume/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Fetch Links from Task using Java - DataForSeo API

Source: https://docs.dataforseo.com/v2/op_csharp=

This Java code snippet demonstrates how to retrieve links associated with a specific task ID and page URL from the DataForSeo API. It utilizes Apache HttpClient to make a GET request and the org.json library to parse the JSON response. This example is a starting point and may require further error handling and configuration for production use.

```java
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.util.*;
public class Demos {
    public static void op_tasks_get_links_from() throws JSONException, IOException {

```

--------------------------------

### Bash: Get App Info Tasks Ready

Source: https://docs.dataforseo.com/v3/app_data/apple/app_info/tasks_ready

This Bash script demonstrates how to authenticate with the DataForSEO API using basic authentication and retrieve a list of ready tasks for app information. It requires `login` and `password` credentials and uses `curl` to make the GET request.

```bash
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access 

login="login" 

password="password" 

cred="$(printf ${login}:${password} | base64)" 

curl --location --request GET "https://api.dataforseo.com/v3/app_data/apple/app_info/tasks_ready" 

--header "Authorization: Basic ${cred}"  

--header "Content-Type: application/json" 

--data-raw ""

```

--------------------------------

### GET /v2/cmn_locations/{country_iso_code}

Source: https://docs.dataforseo.com/v2/cmn_csharp=

Retrieves a list of common locations filtered by a specific country's ISO code. This allows you to get locations relevant to a particular country.

```APIDOC
## GET /v2/cmn_locations/$country_iso_code

### Description
Retrieves a list of common locations filtered by the specified country ISO code. This endpoint is useful for obtaining location data specific to a particular country.

### Method
GET

### Endpoint
`https://api.dataforseo.com/v2/cmn_locations/$country_iso_code`

### Path Parameters

- **`country_iso_code`** (string) - Required - The ISO 3166-1 alpha-2 code of the country for which to retrieve locations (e.g., "US" for United States, "GB" for United Kingdom).

### Query Parameters

- **`gzip`** (integer) - Optional - Set to `1` to enable gzip compression for the response.

### Request Example
```
GET https://api.dataforseo.com/v2/cmn_locations/US?gzip=1
```

### Response
#### Success Response (200)
- **`status`** (string) - Indicates the status of the response, e.g., "ok".
- **`results_time`** (string) - The time taken to process the request in seconds.
- **`results_count`** (integer) - The total number of location results for the specified country.
- **`results`** (array) - An array of location objects for the specified country.
    - **`loc_id`** (integer) - The unique identifier for the location.
    - **`loc_id_parent`** (integer) - The identifier of the parent location, if applicable.
    - **`loc_name`** (string) - The name of the location.
    - **`loc_name_canonical`** (string) - The canonical name of the location, often including parent information.
    - **`loc_type`** (string) - The type of location (e.g., "Country", "DMA Region").
    - **`loc_country_iso_code`** (string) - The ISO 3166-1 alpha-2 code of the country the location belongs to.
    - **`dma_region`** (boolean) - Indicates if the location is a DMA Region.
    - **`kwrd_finder`** (boolean) - Indicates if keyword finder is supported for this location.
    - **`kwrd_finder_lang`** (string) - The language code for keyword finder if supported, otherwise empty.

#### Response Example
```json
{
    "status": "ok",
    "results_time": "0.0215 sec.",
    "results_count": 150,
    "results": [
        {
            "loc_id": 2840,
            "loc_id_parent": null,
            "loc_name": "United States",
            "loc_name_canonical": "United States",
            "loc_type": "Country",
            "loc_country_iso_code": "US",
            "dma_region": false,
            "kwrd_finder": true,
            "kwrd_finder_lang": "en"
        },
        {
            "loc_id": 200662,
            "loc_id_parent": 21176,
            "loc_name": "Abilene-Sweetwater, TX",
            "loc_name_canonical": "Abilene-Sweetwater, TX,Texas,United States",
            "loc_type": "DMA Region",
            "loc_country_iso_code": "US",
            "dma_region": true,
            "kwrd_finder": false,
            "kwrd_finder_lang": ""
        }
    ]
}
```
```

--------------------------------

### Java Example: Get AdWords Status from DataForSeo API

Source: https://docs.dataforseo.com/v2/cmn_csharp=

This Java code snippet illustrates how to retrieve AdWords status information from the DataForSeo API. It utilizes the Apache HttpClient library for making the GET request and org.json for parsing the JSON response. Remember to substitute 'login' and 'password' with your valid DataForSeo API credentials.

```java
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.util.*;
public class Demos {
    public static void cmn_adwords_status() throws JSONException, IOException {
        HttpClient client;
        client = HttpClientBuilder.create().build();
        HttpGet get = new HttpGet("https://api.dataforseo.com/v2/cmn_adwords_status");
        //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
        String basicAuth = Base64.getEncoder().encodeToString(("login:password").getBytes("UTF-8"));
        get.setHeader("Content-type", "application/json");
        get.setHeader("Authorization", "Basic " + basicAuth);
        HttpResponse response = client.execute(get);
        JSONObject obj = new JSONObject(EntityUtils.toString(response.getEntity()));
        if (obj.get("status").equals("error")) {
            System.out.println("error. Code:" + obj.getJSONObject("error").get("code") + " Message: " + obj.getJSONObject("error").get("message"));
        } else {
            JSONArray results = obj.getJSONArray("results");
            if (results.length() > 0) {
                for (int i = 0; i < results.length(); i++) {
                    System.out.println(results.get(i));
                }
            } else {
                System.out.println("no results");
            }
        }
    }
}

```

--------------------------------

### C#: Retrieve Google Product Task Results

Source: https://docs.dataforseo.com/v3/merchant/google/products/task_get/html

This C# example demonstrates how to fetch Google product task results using the DataForSEO API. It initializes an HttpClient, authenticates with basic credentials, retrieves a list of ready tasks, and then iterates to get the HTML results for each completed task. Error handling is included for non-20000 status codes.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task merchant_google_products_task_get()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };

            // #1 - using this method you can get a list of completed tasks

            // GET /v3/merchant/google/products/tasks_ready

            var response = await httpClient.GetAsync("/v3/merchant/google/products/tasks_ready");

            var tasksInfo = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            var tasksResponses = new List<object>();

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (tasksInfo.status_code == 20000)

            {

                if (tasksInfo.tasks != null)

                {

                    foreach (var tasks in tasksInfo.tasks)

                    {

                        if (tasks.result != null)

                        {

                            foreach (var task in tasks.result)

                            {

                                if (task.endpoint_html != null)

                                {

                                    // #2 - using this method you can get results of each completed task

                                    // GET /v3/merchant/google/products/task_get/html/$id

                                    var taskGetResponse = await httpClient.GetAsync((string)task.endpoint_html);

                                    var taskResultObj = JsonConvert.DeserializeObject<dynamic>(await taskGetResponse.Content.ReadAsStringAsync());

                                    if (taskResultObj.tasks != null)

                                    {

                                        var fst = taskResultObj.tasks.First;

                                        // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

                                        if (fst.status_code >= 40000 || fst.result == null)

                                            Console.WriteLine($"error. Code: {fst.status_code} Message: {fst.status_message}");

                                        else

                                            tasksResponses.Add(fst.result);

                                    }

                                    // #3 - another way to get the task results by id

                                    // GET /v3/merchant/google/products/task_get/html/$id

                                    /*

                                    var tasksGetResponse = await httpClient.GetAsync("/v3/merchant/google/products/task_get/html/" + (string)task.id);

                                    var taskResultObj = JsonConvert.DeserializeObject<dynamic>(await tasksGetResponse.Content.ReadAsStringAsync());

                                    if (taskResultObj.tasks != null)

                                    {

                                        var fst = taskResultObj.tasks.First;

                                        // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors


```

--------------------------------

### Get Google Organic SERP Task Results using Node.js (axios)

Source: https://docs.dataforseo.com/v3/serp/google/organic/task_get/html

This JavaScript snippet uses the axios library to make a GET request to retrieve Google Organic SERP task results. It employs basic authentication with username and password. The response data containing the task results is logged to the console. Ensure axios is installed (`npm install axios`).

```javascript
const task_id = '02201650-1073-0066-2000-1d132bb28897';



const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/google/organic/task_get/html/' + task_id,

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});

```

--------------------------------

### Get Google My Business Info via Node.js

Source: https://docs.dataforseo.com/v3/business_data/google/my_business_info/task_get

This Node.js script uses the 'axios' library to make an HTTP GET request to the DataForSEO API. It demonstrates how to authenticate using basic auth (username and password) and retrieve information for a specific task ID. The results are logged to the console. Make sure to install axios (`npm install axios`) and replace 'login', 'password', and the task ID with your actual credentials and the relevant task ID.

```javascript
const task_id = '02231934-2604-0066-2000-570459f04879';



const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/business_data/google/my_business_info/task_get/' + task_id,

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch Google SERP Tasks Ready using Python

Source: https://docs.dataforseo.com/v3/serp/google/dataset_info/task_get/advanced

This Python example shows how to use the `RestClient` class to fetch a list of completed tasks from the DataForSEO API. It requires downloading the `python_Client.zip` file and initializing the client with your API login and password. The code makes a GET request to the `tasks_ready` endpoint.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# 1 - using this method you can get a list of completed tasks
# GET /v3/serp/google/dataset_info/tasks_ready
response = client.get("/v3/serp/google/dataset_info/tasks_ready")
```

--------------------------------

### JavaScript (Node.js): Get Bing Search Volume History Data

Source: https://docs.dataforseo.com/v3/keywords_data/bing/search_volume_history/task_get

This Node.js script uses the 'axios' library to make a GET request to the DataForSEO API for Bing search volume history. It authenticates using basic auth with provided 'login' and 'password'. The script logs the task results or any errors encountered. Ensure you have 'axios' installed (`npm install axios`).

```javascript
const task_id = '02231934-2604-0066-2000-570459f04879';



const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/keywords_data/bing/search_volume_history/task_get/' + task_id,

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### JavaScript (Node.js): Get Google Keyword Suggestions Live

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live_php=

This JavaScript example uses the 'axios' library to perform a POST request to the Dataforseo API for live keyword suggestions. It demonstrates setting up the request with authentication, request body, and headers, and includes basic error handling.

```javascript
const post_array = [];



post_array.push({

  "keyword": "phone",

  "location_code": 2840,

  "language_name": "English",

  "include_serp_info": true,

  "include_seed_keyword": true,

  "limit": 1

});



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/dataforseo_labs/keyword_suggestions/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Set Task Parameters via URL and Postback Data (Python)

Source: https://docs.dataforseo.com/v3/serp/bing/local_pack/task_post

This example shows an alternative method for setting up a task where all required parameters, including the search URL, postback data type (e.g., 'html'), and postback URL, are passed directly within the URL. This approach is useful when you need to specify the exact search query and how results should be returned.

```python
post_data = {}
post_data[len(post_data)] = dict(

    url="https://www.bing.com/search?q=rank%20checker&count=50&first=1&setlang=en&cc=US&safesearch=Moderate&FORM=SEPAGE",

    postback_data="html",

    postback_url="https://your-server.com/postbackscript"

)
```

--------------------------------

### Fetch Ready Tasks with Python

Source: https://docs.dataforseo.com/v3/serp/google/images/tasks_ready_php=

Python example for retrieving ready tasks from the DataForSEO API. It utilizes a custom RestClient class (downloadable from a provided URL) for simplified API interactions. The code initializes the client with credentials and then calls the 'get' method to fetch tasks.

```python
from client import RestClient

# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip

client = RestClient("login", "password")

# using this method you can get a list of completed tasks

# GET /v3/serp/google/images/tasks_ready

# in addition to 'google' and 'images' you can also set other search engine and type parameters

# the full list of possible parameters is available in documentation

response = client.get("/v3/serp/google/images/tasks_ready")
```

--------------------------------

### Fetch Ready Keyword Data Tasks (C#)

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/ad_traffic_by_keywords/tasks_ready_php=

This C# example shows how to authenticate with the DataForSEO API using basic authentication and retrieve a list of completed tasks for keyword data. It uses HttpClient for making the GET request and Newtonsoft.Json for deserializing the JSON response. It includes error handling for non-20000 status codes.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/keywords_data/google_ads/ad_traffic_by_keywords/tasks_ready

            // in addition to 'ad_traffic_by_keywords' you can also set other parameters

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/keywords_data/google_ads/ad_traffic_by_keywords/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Google My Business Info Live via Bash

Source: https://docs.dataforseo.com/v3/business_data/google/my_business_info/live

This Bash script demonstrates how to fetch live Google My Business information using the DataForSEO API. It requires user credentials for authentication and constructs a POST request with specific location and keyword details. The output is the raw API response.

```bash
login="login"

password="password"

cred="$(printf ${login}:${password} | base64)"

curl --location --request POST "https://api.dataforseo.com/v3/business_data/google/my_business_info/live" \

--header "Authorization: Basic ${cred}"  \

--header "Content-Type: application/json" \

--data-raw "[

    {

        "language_code": "en",

        "location_name": "New York,New York,United States",

        "keyword": "RustyBrick, Inc."

    }

]"
```

--------------------------------

### App Data API - Node.js Client Example

Source: https://docs.dataforseo.com/v3/app_data/apple/app_searches/task_get/advanced

Example of how to use the Node.js axios library to fetch advanced app search task results. This snippet shows how to make a GET request with authentication and retrieve the data.

```APIDOC
## App Data API - Node.js Client Example

### Description
Example of how to use the Node.js axios library to fetch advanced app search task results. This snippet shows how to make a GET request with authentication and retrieve the data.

### Method
GET

### Endpoint
/v3/app_data/apple/app_searches/task_get/advanced/{id}

### Parameters
#### Query Parameters
- **task_id** (string) - Required - The ID of the task to retrieve results for.

### Request Example
```javascript
const task_id = '02231934-2604-0066-2000-570459f04879';
const axios = require('axios');
axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/app_data/apple/app_searches/task_get/advanced' + task_id,
    auth: {
        username: 'login',
        password: 'password'
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response['data']['tasks'];
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

### Response
#### Success Response (200)
- **tasks** (array) - An array containing the results for the specified task ID.

#### Response Example
```json
{
  "tasks": [
    {
      "rating_max": 5,
      "is_free": false,
      "price": {
        "current": 4.99,
        "regular": 4.99,
        "max_value": 4.99,
        "currency": "USD"
      },
      "is_price_range": false,
      "displayed_price": "$4.99"
    }
  ]
}
```
```

--------------------------------

### Fetch Trustpilot Reviews Tasks Ready using PHP RestClient

Source: https://docs.dataforseo.com/v3/business_data/trustpilot/reviews/tasks_ready

This PHP example demonstrates how to fetch Trustpilot reviews tasks ready using the provided RestClient. It requires downloading the RestClient.zip file and includes error handling for API requests. Remember to replace 'login' and 'password' with your actual API credentials.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');

try {

    // using this method you can get a list of completed tasks

    // GET /v3/business_data/trustpilot/reviews/tasks_ready

    $result = $client->get('/v3/business_data/trustpilot/reviews/tasks_ready');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### Get Product Info Tasks Ready (PHP)

Source: https://docs.dataforseo.com/v3/merchant/google/product_info/tasks_ready

This PHP script utilizes the RestClient class to interact with the Dataforseo API. It demonstrates how to initialize the client with API credentials and then make a GET request to the /v3/merchant/google/product_info/tasks_ready endpoint to retrieve a list of completed tasks. Error handling for API exceptions is included.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');



try {

   // using this method you can get a list of completed tasks

   // GET /v3/merchant/google/product_info/tasks_ready

   $result = $client->get('/v3/merchant/google/product_info/tasks_ready');

   print_r($result);

   // do something with result

} catch (RestClientException $e) {

   echo "n";

   print "HTTP code: {$e->getHttpCode()}n";

   print "Error code: {$e->getCode()}n";

   print "Message: {$e->getMessage()}n";

   print  $e->getTraceAsString();

   echo "n";

}

$client = null;

?>
```

--------------------------------

### Fetch Google Keyword Ideas using Node.js Axios

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live_php=

This JavaScript example uses the Axios library to fetch Google Keyword Ideas. It demonstrates how to set up authentication using basic auth, construct the request payload, and handle the API response or errors. Ensure Axios is installed (`npm install axios`).

```javascript
const post_array = [];



post_array.push({

  "keywords": [

    "phone",

    "watch"

  ],

  "location_code": 2840,

  "language_name": "English",

  "filters": [

    ["keyword_info.search_volume", ">", 10]

  ],

  "limit": 3



});



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### C#: Post SERP Task (Basic Configuration) - DataForSeo API

Source: https://docs.dataforseo.com/v3/serp/google/local_finder/task_post

This C# example demonstrates how to post a basic SERP task using the DataForSeo API. It configures an HttpClient with authentication and creates a task with essential parameters like language code, location code, and keyword. The response is then deserialized and checked for success.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_task_post()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            // example #1 - a simple way to set a task

            // this way requires you to specify a location, a language of search, and a keyword.

            postData.Add(new

            {

                language_code = "en",

                location_code = 2840,

                keyword = "local nail services",

                min_rating=4.5,

                time_filter="monday"

            });

            // POST /v3/serp/google/local_finder/task_post

            // in addition to 'google' and 'local_finder' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/serp/google/local_finder/task_post", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### API Request Examples (cURL, PHP, Node.js, Python, C#)

Source: https://docs.dataforseo.com/v3/databases/app_store/listings

Provides ready-to-use code samples for making API requests to DataForSEO services. Choose an endpoint from the sidebar to see specific examples in your preferred language.

```bash
curl -X GET "https://api.dataforseo.com/v3/some/endpoint" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

```php
<?php

$apiKey = 'YOUR_API_KEY';
$endpoint = 'https://api.dataforseo.com/v3/some/endpoint';

$ch = curl_init();
c_setopt($ch, CURLOPT_URL, $endpoint);
c_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Authorization: Bearer ' . $apiKey
));
c_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);

if (curl_errno($ch)) {
    echo 'Error:' . curl_error($ch);
}

curl_close($ch);

echo $response;

?>

```

```javascript
const fetch = require('node-fetch');

const apiKey = 'YOUR_API_KEY';
const endpoint = 'https://api.dataforseo.com/v3/some/endpoint';

async function callApi() {
  try {
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    });
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error:', error);
  }
}

callApi();

```

```python
import requests

api_key = 'YOUR_API_KEY'
endpoint = 'https://api.dataforseo.com/v3/some/endpoint'

headers = {
    'Authorization': f'Bearer {api_key}'
}

try:
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print(f'Error: {e}')

```

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

public class DataForSeoClient
{
    private readonly string _apiKey = "YOUR_API_KEY";
    private readonly string _endpoint = "https://api.dataforseo.com/v3/some/endpoint";

    public async Task<string> GetDataAsync()
    {
        using (var client = new HttpClient())
        {
            client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _apiKey);
            
            try
            {
                HttpResponseMessage response = await client.GetAsync(_endpoint);
                response.EnsureSuccessStatusCode(); // Throw if error status
                return await response.Content.ReadAsStringAsync();
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Error: {e.Message}");
                return null;
            }
        }
    }

    public static async Task Main(string[] args)
    {
        var dataForSeoClient = new DataForSeoClient();
        string result = await dataForSeoClient.GetDataAsync();
        if (result != null)
        {
            Console.WriteLine(result);
        }
    }
}

```

--------------------------------

### C#: Fetch and Process SERP Task Results

Source: https://docs.dataforseo.com/v3/serp/seznam/organic/task_get/html

This C# example demonstrates how to fetch and process SERP task results using the DataForSEO API. It includes setting up an HTTP client, handling authentication, retrieving a list of ready tasks, and deserializing responses. It also shows how to get individual task results via HTML endpoint.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_task_get()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // #1 - using this method you can get a list of completed tasks

            // GET /v3/serp/seznam/organic/tasks_ready

            // in addition to 'seznam' and 'organic' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/serp/seznam/organic/tasks_ready");

            var tasksInfo = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            var tasksResponses = new List<object>();

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (tasksInfo.status_code == 20000)

            {

                if (tasksInfo.tasks != null)

                {

                    foreach (var tasks in tasksInfo.tasks)

                    {

                        if (tasks.result != null)

                        {

                            foreach (var task in tasks.result)

                            {

                                if (task.endpoint_html != null)

                                {

                                    // #2 - using this method you can get results of each completed task

                                    // GET /v3/serp/seznam/organic/task_get/html/$id

                                    var taskGetResponse = await httpClient.GetAsync((string)task.endpoint_html);

                                    var taskResultObj = JsonConvert.DeserializeObject<dynamic>(await taskGetResponse.Content.ReadAsStringAsync());

                                    if (taskResultObj.tasks != null)

                                    {

                                        var fst = taskResultObj.tasks.First;

                                        // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

                                        if (fst.status_code >= 40000 || fst.result == null)

                                            Console.WriteLine($"error. Code: {fst.status_code} Message: {fst.status_message}");

                                        else

                                            tasksResponses.Add(fst.result);

                                    }

                                    // #3 - another way to get the task results by id

                                    // GET /v3/serp/seznam/organic/task_get/html/$id

                                    /*

                                    var tasksGetResponse = await httpClient.GetAsync("/v3/serp/seznam/organic/task_get/html/" + (string)task.id);

                                    var tasksResultObj = JsonConvert.DeserializeObject<dynamic>(await tasksGetResponse.Content.ReadAsStringAsync());

                                    if (tasksResultObj.tasks != null)

                                    {

                                        var fst = taskResultObj.tasks.First;

```

--------------------------------

### Get Google Seller Tasks Ready (Bash)

Source: https://docs.dataforseo.com/v3/merchant/google/sellers/tasks_ready

This Bash script demonstrates how to authenticate with the DataForSEO API using basic authentication and retrieve a list of ready tasks for Google sellers. It constructs the authorization header by encoding login and password, then makes a GET request to the specified API endpoint.

```bash
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access 

login="login" 

password="password" 

cred="$(printf ${login}:${password} | base64)" 

curl --location --request GET "https://api.dataforseo.com/v3/merchant/google/sellers/tasks_ready" 

--header "Authorization: Basic ${cred}"  

--header "Content-Type: application/json" 

--data-raw ""
```

--------------------------------

### POST /v3/business_data/google/extended_reviews/task_post (PHP)

Source: https://docs.dataforseo.com/v3/business_data/google/extended_reviews/task_post

This PHP example shows how to use the RestClient to post tasks for retrieving Google Extended Reviews. It includes multiple examples of task configurations, including basic setup with location, language, and keyword, as well as advanced options like priority, depth, and pingback URLs.

```APIDOC
## POST /v3/business_data/google/extended_reviews/task_post (PHP)

### Description
Use the RestClient to submit tasks for collecting Google Extended Reviews. This example provides various ways to configure a task, such as setting search parameters, priority, and callback URLs.

### Method
POST

### Endpoint
https://api.dataforseo.com/v3/business_data/google/extended_reviews/task_post

### Parameters
#### Request Body
An array of task objects. Each object can contain:
- **location_name** (string) - Required - The name of the location.
- **language_name** (string) - Required - The name of the language.
- **keyword** (string) - Required - The search keyword.
- **depth** (integer) - Optional - The depth of reviews to retrieve.
- **priority** (integer) - Optional - The priority of the task (higher value means higher priority).
- **tag** (string) - Optional - A custom tag for the task.
- **pingback_url** (string) - Optional - A URL to send a GET request to upon task completion.
- **postback_url** (string) - Optional - A URL to send the results to upon task completion.

### Request Example
```php
<?php

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';
$login = 'YOUR_LOGIN'; // Replace with your login
$password = 'YOUR_PASSWORD'; // Replace with your password

$client = new RestClient($api_url, null, $login, $password);

$post_array = array();

// Example 1: Basic task setup
$post_array[] = array(
   "location_name" => "London,England,United Kingdom",
    "language_name" => "English",
    "keyword" => mb_convert_encoding("hedonism wines", "UTF-8")
);

// Example 2: Task with advanced parameters
$post_array[] = array(
   "location_name" => "London,England,United Kingdom",
   "language_name" => "English",
   "keyword" => mb_convert_encoding("hedonism wines", "UTF-8"),
   "depth" => 40,
   "priority" => 2,
   "tag" => "some_string_123",
   "pingback_url" => 'https://your-server.com/pingscript?id=$id&tag=$tag'
);

// Example 3: Task with postback URL
$post_array[] = array(
   "location_name" => "London,England,United Kingdom",
   "language_name" => "English",
   "keyword" => mb_convert_encoding("hedonism wines", "UTF-8"),
   "postback_url" => "https://your-server.com/postbackscript"
);

if (count($post_array) > 0) {
   try {
      $result = $client->post('/v3/business_data/google/extended_reviews/task_post', $post_array);
      print_r($result);
   } catch (RestClientException $e) {
      echo "n";
      print "HTTP code: {$e->getHttpCode()}n";
      print "Error code: {$e->getCode()}n";
      print "Message: {$e->getMessage()}n";
      print  $e->getTraceAsString();
      echo "n";
   }
}

$client = null;

?>
```

### Response
#### Success Response (200)
- **tasks** (array) - An array containing the status of the posted tasks.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "0001",
      "status": "Ok"
    }
  ]
}
```
```

--------------------------------

### Get Google Reviews Tasks Ready (C#)

Source: https://docs.dataforseo.com/v3/business_data/google/reviews/tasks_ready

This C# example shows how to fetch a list of completed tasks for Google Reviews using the DataForSEO API. It uses HttpClient to make a GET request and Newtonsoft.Json to deserialize the JSON response. The code checks for a successful status code (20000) and prints the result or an error message.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task business_data_google_reviews_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/business_data/google/reviews/tasks_ready

            var response = await httpClient.GetAsync("/v3/business_data/google/reviews/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Google Seller Tasks Ready (Node.js)

Source: https://docs.dataforseo.com/v3/merchant/google/sellers/tasks_ready

This Node.js example uses the 'axios' library to fetch data from the DataForSEO API. It demonstrates making a GET request to the Google sellers tasks endpoint, including authentication credentials in the request and handling the response or any errors. The result data from the first task is logged to the console.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/merchant/google/sellers/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get SERP Tasks Ready Status (C#)

Source: https://docs.dataforseo.com/v3/serp/google/finance_ticker_search/tasks_ready

This C# code example uses HttpClient to make a GET request to the /v3/serp/google/finance_ticker_search/tasks_ready endpoint. It deserializes the JSON response using Newtonsoft.Json and checks the 'status_code' to determine if the tasks are ready or if an error occurred. It requires the Newtonsoft.Json and System.Net.Http namespaces.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/serp/google/finance_ticker_search/tasks_ready

            // in addition to 'google' and 'finance_ticker_search' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/serp/google/finance_ticker_search/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Appendix Errors List via Node.js

Source: https://docs.dataforseo.com/v3/appendix/errors_php=

This Node.js example uses the axios library to make a GET request to the DataForSEO API to retrieve appendix errors. Authentication is handled via the 'auth' object in the request configuration.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/appendix/errors',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch Google Ads Search Tasks Ready (PHP)

Source: https://docs.dataforseo.com/v3/serp/google/ads_search/tasks_ready_php=

This PHP example utilizes the RestClient class to interact with the DataForSEO API. It shows how to initialize the client with API credentials, make a GET request to retrieve completed Google Ads search tasks, and handle potential exceptions. You'll need to download the RestClient.php file separately. Replace 'login' and 'password' with your credentials.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {

    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

    $client = new RestClient($api_url, null, 'login', 'password');

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

    exit();

}

try {

    // using this method you can get a list of completed tasks

    // GET /v3/serp/google/ads_search/tasks_ready

    // in addition to 'google' and 'ads_search' you can also set other search engine and type parameters

    // the full list of possible parameters is available in documentation

    $result = $client->get('/v3/serp/google/ads_search/tasks_ready');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### Fetch Keyword Finder Locations using C#

Source: https://docs.dataforseo.com/v2/cmn_csharp=

This C# code demonstrates fetching keyword finder locations via the DataForSEO API using HttpClient. It requires Newtonsoft.Json for JSON deserialization and uses basic authentication with your API credentials. The example is an asynchronous task that makes a GET request to the specified endpoint.

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task cmn_locations_stat_kwrd_finder()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };
            var response = await httpClient.GetAsync("v2/cmn_locations_stat_kwrd_finder");

```

--------------------------------

### GET /serp/naver/organic/tasks_ready

Source: https://docs.dataforseo.com/v3/serp/naver/organic/tasks_ready

A specific example endpoint for retrieving completed tasks for Naver organic search. This is a pre-defined endpoint for convenience.

```APIDOC
## GET /serp/naver/organic/tasks_ready

### Description
Retrieves a list of completed tasks specifically for Naver organic search results that are ready for collection. This is a specialized endpoint for Naver organic search.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/serp/naver/organic/tasks_ready

### Parameters

#### Query Parameters
None

### Request Example
None (GET request with no body)

### Response
#### Success Response (200)
- **version** (string) - the current version of the API
- **status_code** (integer) - general status code
- **status_message** (string) - general informational message
- **time** (string) - execution time, seconds
- **cost** (float) - total tasks cost, USD
- **tasks_count** (integer) - the number of tasks in the `tasks` array
- **tasks_error** (integer) - the number of tasks in the `tasks` array returned with an error
- **tasks** (array) - array of tasks. Each task object contains:
  - **id** (string) - task identifier (UUID format)
  - **status_code** (integer) - status code of the task
  - **status_message** (string) - informational message of the task
  - **time** (string) - execution time, seconds
  - **cost** (float) - cost of the task, USD
  - **result_count** (integer) - number of elements in the `result` array
  - **path** (array) - URL path
  - **data** (object) - contains the parameters passed in the request’s URL
  - **result** (array) - array of results. Each result object contains:
    - **id** (string) - task identifier of the completed task (UUID format)
    - **se** (string) - search engine specified when setting the task
    - **se_type** (string) - type of search engine (e.g., `organic`)
    - **date_posted** (string) - date when the task was posted (UTC format)
    - **tag** (string) - user-defined task identifier
    - **endpoint_regular** (string) - URL for collecting the results of the SERP Regular task (or `null`)
    - **endpoint_advanced** (string) - URL for collecting the results of the SERP Advanced task (or `null`)
    - **endpoint_html** (string) - URL for collecting the results of the SERP HTML task (or `null`)

#### Response Example
```json
{
  "version": "v3",
  "status_code": 200,
  "status_message": "ok",
  "time": "0.008",
  "cost": 0.00003,
  "tasks_count": 2,
  "tasks_error": 0,
  "tasks": [
    {
      "id": "uuid-task-3",
      "status_code": 200,
      "status_message": "Success",
      "time": "0.003",
      "cost": 0.000015,
      "result_count": 5,
      "path": [
        "serp",
        "naver",
        "organic"
      ],
      "data": {
        "keyword": "naver search"
      },
      "result": [
        {
          "id": "uuid-result-3",
          "se": "naver",
          "se_type": "organic",
          "date_posted": "2023-10-27T12:00:00+00:00",
          "tag": "naver_tag",
          "endpoint_regular": "https://api.dataforseo.com/v3/serp/naver/organic/task_get?id=uuid-task-3",
          "endpoint_advanced": null,
          "endpoint_html": null
        }
      ]
    }
  ]
}
```
```

--------------------------------

### Fetch Ready Tasks using PHP

Source: https://docs.dataforseo.com/v3/serp/google/jobs/tasks_ready

This PHP example demonstrates how to use the provided RestClient class to fetch a list of completed tasks from the 'tasks_ready' endpoint. It shows basic error handling for API requests and how to print the results. Ensure you have the RestClient.php file included.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {

    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

    $client = new RestClient($api_url, null, 'login', 'password');

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

    exit();

}

try {

    // using this method you can get a list of completed tasks

    // GET /v3/serp/google/jobs/tasks_ready

    // in addition to 'google' and 'jobs' you can also set other search engine and type parameters

    // the full list of possible parameters is available in documentation

    $result = $client->get('/v3/serp/google/jobs/tasks_ready');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### GET /v3/business_data/tripadvisor/search/tasks_ready (PHP)

Source: https://docs.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready

This PHP example shows how to use the RestClient to fetch completed TripAdvisor search tasks. It includes error handling for API requests.

```APIDOC
## GET /v3/business_data/tripadvisor/search/tasks_ready (PHP)

### Description
Retrieves a list of completed tasks for TripAdvisor searches using the PHP RestClient.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```php
<?php

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';
$login = 'your_login';
$password = 'your_password';

$client = new RestClient($api_url, null, $login, $password);

try {
    $result = $client->get('/v3/business_data/tripadvisor/search/tasks_ready');
    print_r($result);
} catch (RestClientException $e) {
    echo "n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "n";
}

$client = null;

?>
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "status_code": 200,
      "status_message": "Success",
      "time_taken": "0.123s",
      "result_count": 1,
      "path": [
        "business_data",
        "tripadvisor",
        "search"
      ],
      "data": [],
      "info": {
        "count": 1,
        "time_taken": "0.123s"
      },
      "cost": 0.001
    }
  ]
}
```
```

--------------------------------

### GET /v2/cmn_locations_stat_kwrd_finder

Source: https://docs.dataforseo.com/v2/cmn

Retrieves common location statistics for keyword finder. Includes setup for HttpClient with authentication and response handling.

```APIDOC
## GET /v2/cmn_locations_stat_kwrd_finder

### Description
This endpoint retrieves common location statistics for keyword finder functionality. The provided C# code demonstrates how to set up an HttpClient with basic authentication and process the JSON response, including error handling.

### Method
GET

### Endpoint
https://api.dataforseo.com/v2/cmn_locations_stat_kwrd_finder

### Parameters

#### Query Parameters
This endpoint does not explicitly define query parameters in the provided code, but typical keyword finder APIs might include parameters for keywords, location, language, etc.

#### Request Body
This endpoint uses the GET method, so no request body is expected.

### Request Example
(No request body for GET)

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the request (e.g., "ok" or "error").
- **results** (array) - An array containing the statistical results for the keyword finder.

#### Error Response
- **status** (string) - "error"
- **error** (object)
  - **code** (integer) - The error code.
  - **message** (string) - A message describing the error.

#### Response Example
```json
{
    "status": "ok",
    "results": [
        "result1",
        "result2"
    ]
}
```

#### Error Example
```json
{
    "status": "error",
    "error": {
        "code": 12,
        "message": "Invalid API key"
    }
}
```
```

--------------------------------

### Get Business Listing Categories using Node.js

Source: https://docs.dataforseo.com/v3/business_data/business_listings/categories

This Node.js example utilizes the 'axios' library to make a GET request for business listing categories. It handles both successful responses and errors.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/business_data/business_listings/categories',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});

```

--------------------------------

### Search Business Listings Live - Node.js

Source: https://docs.dataforseo.com/v3/app_data/apple/app_listings/search/live

This Node.js example uses the 'axios' library to make a POST request to search for business listings. It demonstrates setting up authentication using basic auth and sending a JSON payload. The response data is logged to the console, and errors are caught and logged.

```javascript
const post_array = [];



post_array.push({

    "title": "vpn",

    "description": "vpn",

    "categories": [

      "Tools"

    ],

    "order_by": [

      "item.rating.value,desc"

    ],

    "filters": [

      [

        "item.rating.value",

        ">",

        4.5

      ]

    ],

    "limit": 10

  });



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/business_data/business_listings/search/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Initialize DataForSEO Client and Get Tasks (Python)

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/task_get_php=

This snippet demonstrates initializing the DataForSEO RestClient with provided login and password, and then making a GET request to retrieve a list of completed tasks for keyword data. It highlights that additional parameters can be set to filter tasks, with the full list available in the documentation.

```python
client = RestClient("login", "password")

# 1 - using this method you can get a list of completed tasks

# in addition to 'keywords_for_site' you can also set other parameters

# the full list of possible parameters is available in documentation

# GET /v3/keywords_data/google_ads/keywords_for_site/tasks_ready

response = client.get("/v3/keywords_data/google_ads/keywords_for_site/tasks_ready")

```

--------------------------------

### Initialize DataForSEO API Client and Get Tasks Ready via Python

Source: https://docs.dataforseo.com/v3/merchant/google/sellers/task_get/advanced_php=

This Python snippet shows how to initialize the RestClient for the DataForSEO API with login credentials. It then demonstrates how to call the `/v3/merchant/google/sellers/tasks_ready` endpoint to get a list of completed tasks. Requires the python_Client.zip.

```python
from client import RestClient

# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip

client = RestClient("login", "password")

# 1 - using this method you can get a list of completed tasks

# GET /v3/merchant/google/sellers/tasks_ready

response = client.get("/v3/merchant/google/sellers/tasks_ready")

```

--------------------------------

### Fetch Ready App List Tasks using Python

Source: https://docs.dataforseo.com/v3/app_data/google/app_list/tasks_ready

This Python snippet demonstrates fetching a list of ready tasks for app data from the DataForSEO API using a provided RestClient. It requires the 'client' module and your API login and password. The example shows a basic GET request.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# using this method you can get a list of completed tasks
# GET /v3/app_data/google/app_list/tasks_ready
response = client.get("/v3/app_data/google/app_list/tasks_ready")
```

--------------------------------

### GET /v3/keywords_data/bing/search_volume/tasks_ready

Source: https://docs.dataforseo.com/v3/keywords_data/bing/search_volume/tasks_ready

This endpoint retrieves a list of completed tasks. The examples demonstrate its usage with PHP, Axios (JavaScript), and Python clients.

```APIDOC
## GET /v3/keywords_data/bing/search_volume/tasks_ready

### Description
This endpoint retrieves a list of completed tasks related to Bing search volume data. It is designed to be used with the provided RestClient libraries in PHP and Python, or with Axios in JavaScript.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/keywords_data/bing/search_volume/tasks_ready

### Parameters
(No explicit parameters are listed for this GET request in the provided examples, but the RestClient libraries may handle authentication parameters)

### Request Example

**PHP:**
```php
$result = $client->get('/v3/keywords_data/bing/search_volume/tasks_ready');
print_r($result);
```

**JavaScript (Axios):**
```javascript
axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/keywords_data/bing/search_volume/tasks_ready',
    auth: {
        username: 'login',
        password: 'password'
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response['data']['tasks'][0]['result'];
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

**Python:**
```python
response = client.get("/v3/keywords_data/bing/search_volume/tasks_ready")
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks.
  - **result** (object) - The result data for a completed task.

#### Response Example
```json
{
  "tasks_ready": [
    {
      "id": "0123456789",
      "keyword_data": {
        "keyword": "example keyword",
        "search_volume": 1000
      }
    }
  ]
}
```
```

--------------------------------

### Retrieve Google My Business Info Tasks Ready (C#)

Source: https://docs.dataforseo.com/v3/business_data/google/my_business_info/tasks_ready

This C# example shows how to asynchronously retrieve a list of completed tasks for Google My Business information using the DataForSEO API. It includes setting up an HTTP client with authorization, making a GET request, and deserializing the JSON response. Error handling is included to display status code and message on failure.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task business_data_info_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/business_data/google/my_business_info/tasks_ready

            var response = await httpClient.GetAsync("/v3/business_data/google/my_business_info/tasks_ready");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### C#: Make Authenticated HTTP Request for Google App Reviews Tasks Ready

Source: https://docs.dataforseo.com/v3/app_data/google/app_reviews/tasks_ready

This C# code example shows how to set up an HttpClient to make a GET request to the DataForSEO API for 'app_data/google/app_reviews/tasks_ready'. It includes basic authentication using 'login' and 'password' and deserializes the JSON response. The snippet also includes error handling based on the 'status_code' in the response.

```csharp
using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task app_data_google_app_reviews_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/app_data/google/app_reviews/tasks_ready

            var response = await httpClient.GetAsync("/v3/app_data/google/app_reviews/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### GET /v2/cmn_adwords_status

Source: https://docs.dataforseo.com/v2/cmn_csharp=

Retrieves the AdWords status information. You need to use your DataForSEO account credentials for authentication.

```APIDOC
## GET /v2/cmn_adwords_status

### Description
Retrieves the current status of AdWords services. This endpoint is useful for monitoring the availability and operational status of your AdWords campaigns managed through DataForSEO.

### Method
GET

### Endpoint
/v2/cmn_adwords_status

### Parameters
#### Query Parameters
None

#### Request Body
None

### Authentication
Basic authentication using your DataForSEO login and password.

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the request, e.g., "ok".
- **cost** (number) - The cost of the API request.
- **result** (object) - Contains the AdWords status details.
  - **adwords_api_status** (string) - The status of the AdWords API connection.
  - **adwords_account_status** (string) - The status of your AdWords account.

#### Response Example
```json
{
  "status": "ok",
  "cost": 0.0001,
  "result": {
    "adwords_api_status": "available",
    "adwords_account_status": "active"
  }
}
```

#### Error Response (401, 403, 500, etc.)
- **status** (string) - Indicates the status of the request, e.g., "error".
- **error** (object) - Contains error details.
  - **error_code** (integer) - The error code.
  - **message** (string) - A description of the error.
  - **details** (string) - Additional details about the error.

#### Error Response Example
```json
{
  "status": "error",
  "error": {
    "error_code": 401,
    "message": "Unauthorized. Invalid credentials.",
    "details": "Authentication failed. Please check your login and password."
  }
}
```
```

--------------------------------

### Search App Listings via API (Python)

Source: https://docs.dataforseo.com/v3/app_data/google/app_listings/search/live_bash=

This Python example uses the provided RestClient class to search for app listings through the DataForSEO API. It shows how to initialize the client with credentials, define the search parameters in a dictionary, and send a POST request to the live search endpoint. The response from the API is then available for further processing.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    title="vpn",
    description="vpn",
    order_by=["item.rating.value,asc"],
    filters=[
        ["item.rating.value",">",4]

    ],
    limit=3
)

# POST /v3/app_data/google/app_listings/search/live
# POST /v3/app_data/apple/app_listings/search/live
response = client.post("/v3/app_data/google/app_listings/search/live", post_data)
```

--------------------------------

### Get Business Listings Locations API

Source: https://docs.dataforseo.com/v3/business_data/business_listings/locations

This Node.js example uses the axios library to make a GET request to the DataForSEO API for business listing locations. It includes authentication and demonstrates how to process the response.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/business_data/business_listings/locations',

    auth: {

        username: 'login',

        password: 'password'

    },

    data: [{

        country: "us"

    }],

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Live Tasks Sandbox Examples

Source: https://docs.dataforseo.com/v3/appendix/sandbox_php=

Examples of sandbox URLs for various Live tasks across different DataForSEO APIs. These demonstrate the standard structure for accessing Live API endpoints in the sandbox.

```APIDOC
## Live Tasks Sandbox Examples

### Description
This section provides example URLs for accessing various Live API endpoints within the sandbox environment. To use these, replace the base URL with the sandbox equivalent ('sandbox.dataforseo.com').

### Method
GET

### Endpoint Examples
- `https://sandbox.dataforseo.com/v3/keywords_data/google/search_volume/live`
- `https://sandbox.dataforseo.com/v3/serp/google/organic/live/regular`
- `https://sandbox.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live`
- `https://sandbox.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live`
- `https://sandbox.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live`
- `https://sandbox.dataforseo.com/v3/backlinks/referring_domains/live`

### Parameters
(Specific parameters for each live endpoint are not detailed here, but would typically be included in individual endpoint documentation.)

### Request Example
(No request body example provided)

### Response
#### Success Response (200)
(No success response details provided)

#### Response Example
(No response example provided)
```

--------------------------------

### Live LLM Mentions Search - Example Task Setup (Python)

Source: https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/search/live

This Python snippet demonstrates how to set up a task for the Live LLM Mentions Search endpoint. It includes examples of specifying both 'domain' and 'keyword' entities within the 'target' array. The API call is made using the 'requests' library.

```python
import requests
import json

api_url = "https://api.dataforseo.com/v3/ai_optimization/llm_mentions/search/live"

# Example task with a domain entity
task_domain = {
    "target": [
        {
            "domain": "en.wikipedia.org",
            "search_filter": "exclude",
            "search_scope": ["sources"]
        }
    ],
    "location_name": "United States",
    "language_name": "en"
}

# Example task with a keyword entity
task_keyword = {
    "target": [
        {
            "keyword": "bmw",
            "search_filter": "include",
            "search_scope": ["question"],
            "match_type": "partial_match"
        }
    ],
    "location_name": "United States",
    "language_name": "en"
}

# Example task with multiple entities
task_multiple = {
    "target": [
        {
            "domain": "en.wikipedia.org",
            "search_filter": "exclude"
        },
        {
            "keyword": "bmw",
            "match_type": "partial_match",
            "search_scope": ["answer"]
        }
    ],
    "location_name": "United States",
    "language_name": "en"
}

# Choose one task to send or combine them if your plan allows (note: API call can contain only one task)
payload = {
    "task": task_keyword  # Or task_domain, task_multiple
}

headers = {
    "Authorization": "Basic YOUR_API_KEY",
    "Content-Type": "application/json"
}

response = requests.post(api_url, headers=headers, json=payload)

if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

```

--------------------------------

### Fetch SERP Tasks using Node.js (axios)

Source: https://docs.dataforseo.com/v3/serp/seznam/organic/tasks_fixed

This Node.js snippet uses the axios library to fetch completed SERP tasks. It demonstrates making a GET request with authentication and setting headers. Install axios using 'npm install axios'. Replace 'login' and 'password' with your API credentials.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/seznam/organic/tasks_fixed',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### GET /v2/cmn_user

Source: https://docs.dataforseo.com/v2/cmn_csharp=

Retrieves user account information, including limits, balance, and pricing details for various services.

```APIDOC
## GET /v2/cmn_user

### Description
This endpoint retrieves comprehensive details about the user's account, such as their login credentials, timezone, rate limits, current balance, available credits, and pricing information for different API tasks like rank tracking and SERP analysis.

### Method
GET

### Endpoint
https://api.dataforseo.com/v2/cmn_user

### Parameters

#### Query Parameters
This endpoint does not have any query parameters.

#### Request Body
This endpoint does not accept a request body.

### Request Example
```bash
curl -X GET "https://api.dataforseo.com/v2/cmn_user" \
     -H "Authorization: Basic YOUR_BASIC_AUTH_STRING"
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the request, e.g., "ok".
- **results_time** (string) - The time taken to process the request.
- **results_count** (integer) - The number of results returned.
- **results** (array) - An array containing user account details.
  - **login** (string) - The user's login name.
  - **timezone** (string) - The user's timezone.
  - **rate_limit_per_minute** (integer) - The number of requests allowed per minute.
  - **rate** (integer) - Current rate information.
  - **rate_max** (integer) - Maximum rate information.
  - **credit** (integer) - Available credits.
  - **balance** (float) - Current account balance.
  - **count_total** (float) - Total count of items.
  - **count_rnk** (integer) - Count for rank tracking tasks.
  - **count_srp** (float) - Count for SERP analysis tasks.
  - **count_kwrd** (integer) - Count for keyword tasks.
  - **count_pg** (integer) - Count for page tasks.
  - **count_cmp** (integer) - Count for comparison tasks.
  - **price** (object) - Pricing details for various API tasks.
    - **apiRnk** (object) - Pricing for Rank Tracking API.
      - **rnk_tasks_post** (object) - Pricing for posting rank tasks.
        - **priority_low** (object) - Pricing for low priority.
          - **price_type** (string) - Type of pricing (e.g., "per_result").
          - **price** (integer) - Price per result.
        - **priority_normal** (object) - Pricing for normal priority.
          - **price_type** (string) - Type of pricing (e.g., "per_result").
          - **price** (integer) - Price per result.
        - **priority_high** (object) - Pricing for high priority.
          - **price_type** (string) - Type of pricing (e.g., "per_result").
          - **price** (integer) - Price per result.
        - **priority_vip** (object) - Pricing for VIP priority.
          - **price_type** (string) - Type of pricing (e.g., "per_result").
          - **price** (integer) - Price per result.
    - **apiSrp** (object) - Pricing for SERP API.
      - **srp_tasks_post** (object) - Pricing for posting SERP tasks.
        - **priority_low** (object) - Pricing for low priority.
          - **price_type** (string) - Type of pricing (e.g., "per_result").
          - **price** (integer) - Price per result.
        - **priority_normal** (object) - Pricing for normal priority.
          - **price_type** (string) - Type of pricing (e.g., "per_result").
          - **price** (integer) - Price per result.
        - **priority_high** (object) - Pricing for high priority.
          - **price_type** (string) - Type of pricing (e.g., "per_result").
          - **price** (integer) - Price per result.
        - **priority_vip** (object) - Pricing for VIP priority.
          - **price_type** (string) - Type of pricing (e.g., "per_result").
          - **price** (integer) - Price per result.
      - **srp_100** (object) - Pricing for SERP 100 results.
        - **priority_low** (object) - Pricing for low priority.
          - **price_type** (string) - Type of pricing (e.g., "per_request").
          - **price** (integer) - Price per request.
        - **priority_normal** (object) - Pricing for normal priority.
          - **price_type** (string) - Type of pricing (e.g., "per_request").
          - **price** (integer) - Price per request.
        - **priority_high** (object) - Pricing for high priority.
          - **price_type** (string) - Type of pricing (e.g., "per_request").
          - **price** (integer) - Price per request.
        - **priority_vip** (object) - Pricing for VIP priority.
          - **price_type** (string) - Type of pricing (e.g., "per_request").
          - **price** (integer) - Price per request.

#### Error Response (400s/500s)
- **status** (string) - Indicates the status of the request, e.g., "error".
- **error** (object) - Contains error details.
  - **code** (integer) - The error code.
  - **message** (string) - A description of the error.

### Response Example
```json
{
    "status": "ok",
    "results_time": "0.0173 sec.",
    "results_count": 1,
    "results": [
        {
            "login": "superlogin",
            "timezone": "Europe/London",
            "rate_limit_per_minute": 1000,
            "rate": 1,
            "rate_max": 123,
            "credit": 99999999,
            "balance": 99987531.5,
            "count_total": 12467.5,
            "count_rnk": 1466,
            "count_srp": 9149.5,
            "count_kwrd": 3047,
            "count_pg": 0,
            "count_cmp": 0,
            "price": {
                "apiRnk": {
                    "rnk_tasks_post": {
                        "priority_low": {
                            "price_type": "per_result",
                            "price": 1
                        },
                        "priority_normal": {
                            "price_type": "per_result",
                            "price": 1
                        },
                        "priority_high": {
                            "price_type": "per_result",
                            "price": 2
                        },
                        "priority_vip": {
                            "price_type": "per_result",
                            "price": 5
                        }
                    }
                },
                "apiSrp": {
                    "srp_tasks_post": {
                        "priority_low": {
                            "price_type": "per_result",
                            "price": 0
                        },
                        "priority_normal": {
                            "price_type": "per_result",
                            "price": 0
                        },
                        "priority_high": {
                            "price_type": "per_result",
                            "price": 2
                        },
                        "priority_vip": {
                            "price_type": "per_result",
                            "price": 5
                        }
                    },
                    "srp_100": {
                        "priority_low": {
                            "price_type": "per_request",
                            "price": 1
                        },
                        "priority_normal": {
                            "price_type": "per_request",
                            "price": 1
                        },
                        "priority_high": {
                            "price_type": "per_request",
                            "price": 1
                        },
                        "priority_vip": {
                            "price_type": "per_request",
                            "price": 1
                        }
                    }
                }
            }
        }
    ]
}
```
```

--------------------------------

### GET /v3/business_data/tripadvisor/search/tasks_ready (cURL)

Source: https://docs.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready

This example demonstrates how to fetch a list of completed tasks for TripAdvisor searches using cURL. It includes authentication details and request headers.

```APIDOC
## GET /v3/business_data/tripadvisor/search/tasks_ready (cURL)

### Description
Retrieves a list of completed tasks for TripAdvisor searches.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```bash
curl --location --request GET "https://api.dataforseo.com/v3/business_data/tripadvisor/search/tasks_ready" \
--header "Authorization: Basic <encoded_credentials>" \
--header "Content-Type: application/json"
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks.

#### Response Example
```json
{
  "tasks": [
    {
      "id": "01234567-89ab-cdef-0123-456789abcdef",
      "status_code": 200,
      "status_message": "Success",
      "time_taken": "0.123s",
      "result_count": 1,
      "path": [
        "business_data",
        "tripadvisor",
        "search"
      ],
      "data": [],
      "info": {
        "count": 1,
        "time_taken": "0.123s"
      },
      "cost": 0.001
    }
  ]
}
```
```

--------------------------------

### PHP: Create Ranking Task using Website URL

Source: https://docs.dataforseo.com/v2/rnk_csharp=

This example demonstrates the simplest way to set up a ranking task by providing a website URL and a search engine URL. The API will internally determine the search engine and location IDs. This method has limitations and does not support 'map pack', 'maps', or 'mobile' searches.

```php
$post_array = array();

// example #1 - simplest
// you set only a website URL and a search engine URL.
// This search engine URL string will be searched, compared to our internal parameters
// and used as:
// "se_id", "loc_id", "key_id" ( actual and fresh list can be found here: "se_id":
// https://api.dataforseo.com/v2/cmn_se , "loc_id": https://api.dataforseo.com/v2/cmn_locations ) (see example #3 for details)
// If a task was set successfully, this *_id will be returned in results: 'v2/rnk_tasks_post' so you can use it.
// The setting of a task can fail, if you set not-existent search engine, for example.
// Disadvantages: You cannot work with "map pack", "maps", "mobile"
$my_unq_id = mt_rand(0, 30000000); // your unique ID. we will return it with all results. you can set your database ID, string, etc.
$post_array[$my_unq_id] = array(
    "priority" => 1,
    "site" => "dataforseo.com",
    "url" => "https://www.google.co.uk/search?q=seo%20data%20api&hl=en&gl=GB&uule=w+CAIQIFISCXXeIa8LoNhHEZkq1d1aOpZS"
);
```

--------------------------------

### Fetch Google Organic Live Results (JavaScript/Node.js)

Source: https://docs.dataforseo.com/v3/appendix/ai_optimized_response

This Node.js example utilizes the `axios` library to send a POST request to the DataForSEO API for live Google organic results. It demonstrates authentication using basic auth and sending JSON data. Ensure you have `axios` installed (`npm install axios`).

```javascript
const axios = require('axios');



axios({

    method: 'post',

    url: 'https://api.dataforseo.com/v3/serp/google/organic/live/regular.ai',

    auth: {

        username: 'login',

        password: 'password'

    },

    data: [{

        "keyword": encodeURI("albert einstein"),

        "language_code": "en",

        "location_code": 2840

    }],

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get Available Audits with C# HttpClient

Source: https://docs.dataforseo.com/v3/on_page/lighthouse/audits

This C# example demonstrates how to make a GET request to the /v3/on_page/lighthouse/audits endpoint using HttpClient. It includes setting up authentication headers and deserializing the JSON response using Newtonsoft.Json.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_locations()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of available audits

            var response = await httpClient.GetAsync("/v3/on_page/lighthouse/audits");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### C#: Post SERP Task (Advanced Configuration) - DataForSeo API

Source: https://docs.dataforseo.com/v3/serp/google/local_finder/task_post

This C# example shows how to post a SERP task with advanced options, including priority, a tag for tracking, and a pingback URL for notifications. It uses language name and location name for task configuration. The response handling is similar to the basic example.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_task_post()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            // example #2 - a way to set a task with additional parameters

            // high priority allows us to complete a task faster, but you will be charged more credits.

            // after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.

            postData.Add(new

            {

                language_name = "English",

                location_name = "United States",

                keyword = "local nail services",

                min_rating=4.5,

                time_filter="monday",

                priority = 2,

                tag = "some_string_123",

                pingback_url = "https://your-server.com/pingscript?id=$id&tag=$tag"

            });

            // POST /v3/serp/google/local_finder/task_post

            // in addition to 'google' and 'local_finder' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/serp/google/local_finder/task_post", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Google Review Tasks Ready (JavaScript)

Source: https://docs.dataforseo.com/v3/business_data/google/reviews/tasks_ready

This JavaScript example uses the 'axios' library to make a GET request to the DataForSEO API for Google review tasks. It authenticates using basic auth with provided login and password, sets the content type header, and logs the results or errors to the console.

```javascript
const axios = require('axios');

const login = 'login'; // Replace with your login
const password = 'password'; // Replace with your password

axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/business_data/google/reviews/tasks_ready',
    auth: {
        username: login,
        password: password
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    // Accessing the result data, assuming tasks is an array and we want the first task's result
    var result = response.data.tasks && response.data.tasks.length > 0 ? response.data.tasks[0].result : null;
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

--------------------------------

### Get Google Shopping Languages List (Node.js)

Source: https://docs.dataforseo.com/v3/merchant/google/languages

This Node.js example uses the axios library to make a GET request to the DataForSEO API for Google Shopping languages. It demonstrates how to handle the response and potential errors.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/merchant/google/languages',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch SERP Tasks Ready with Python

Source: https://docs.dataforseo.com/v3/serp/seznam/organic/task_get/html

Uses a custom RestClient to retrieve a list of completed SERP tasks. This example demonstrates how to initialize the client with credentials and make a GET request to the 'tasks_ready' endpoint. Ensure the client.py file is available.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# 1 - using this method you can get a list of completed tasks
# GET /v3/serp/seznam/organic/tasks_ready
# in addition to 'seznam' and 'organic' you can also set other search engine and type parameters
# the full list of possible parameters is available in documentation
response = client.get("/v3/serp/seznam/organic/tasks_ready")

```

--------------------------------

### DataforSEO API Access Example (C#)

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live

This C# example shows how to construct an authenticated request to the DataforSEO API. It includes setting the necessary authorization header using your API credentials.

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

public class DataforseoApiClient
{
    public static async Task GetDataAsync()
    {
        // Instead of ‘login’ and ‘password’ use your credentials from https://app.dataforseo.com/api-access
        string login = "login";
        string password = "password";

        using (var httpClient = new HttpClient())
        {
            string credentials = Convert.ToBase64String(Encoding.ASCII.GetBytes($"{login}:{password}"));
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", credentials);

            var response = await httpClient.GetAsync("https://api.dataforseo.com/v3/...");
            response.EnsureSuccessStatusCode();

            var responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseBody);
        }
    }
}
```

--------------------------------

### Get Live Backlinks Count (C#)

Source: https://docs.dataforseo.com/v3/backlinks/bulk_backlinks/live

C# example of how to consume the Bulk Backlinks API to get live backlink counts. This code uses HttpClient to send a POST request with JSON payload.

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

public class BulkBacklinksApiClient
{
    public static async Task Main(string[] args)
    {
        using (var httpClient = new HttpClient())
        {
            string apiUrl = "https://api.dataforseo.com/v3/backlinks/bulk_backlinks/live";
            string credentials = "your_login:your_password"; // Replace with your credentials
            string encodedCredentials = Convert.ToBase64String(Encoding.ASCII.GetBytes(credentials));

            httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", encodedCredentials);
            httpClient.DefaultRequestHeaders.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));

            var payload = new
            {
                targets = new[]
                {
                    "forbes.com",
                    "cnn.com",
                    "bbc.com",
                    "yelp.com",
                    "https://www.apple.com/iphone/",
                    "https://ahrefs.com/blog/",
                    "ibm.com",
                    "https://variety.com/",
                    "https://stackoverflow.com/",
                    "www.trustpilot.com"
                },
                tag = "my_task_01"
            };

            var jsonPayload = Newtonsoft.Json.JsonConvert.SerializeObject(payload);
            var httpContent = new StringContent(jsonPayload, Encoding.UTF8, "application/json");

            HttpResponseMessage response = await httpClient.PostAsync(apiUrl, httpContent);
            string responseBody = await response.Content.ReadAsStringAsync();

            Console.WriteLine(responseBody);
        }
    }
}

```

--------------------------------

### GET /v3/serp/google/ads_search/tasks_ready (PHP)

Source: https://docs.dataforseo.com/v3/serp/google/ads_search/tasks_ready_php=

This PHP example shows how to use the RestClient to fetch completed tasks for Google Ads search. It includes error handling for API requests.

```APIDOC
## GET /v3/serp/google/ads_search/tasks_ready

### Description
Retrieves a list of completed tasks for Google Ads search using the PHP RestClient.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/serp/google/ads_search/tasks_ready

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {
    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
    $client = new RestClient($api_url, null, 'login', 'password');
} catch (RestClientException $e) {
    echo "n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "n";
    exit();
}

try {
    // using this method you can get a list of completed tasks
    $result = $client->get('/v3/serp/google/ads_search/tasks_ready');
    print_r($result);
} catch (RestClientException $e) {
    echo "n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "n";
}

$client = null;

?>
```

### Response
#### Success Response (200)
- **tasks** (array) - An array of completed tasks.
  - **id** (string) - The ID of the task.
  - **result** (object) - The result of the task.

#### Response Example
```php
Array
(
    [tasks] => Array
        (
            [0] => Array
                (
                    [id] => 01234567-89ab-cdef-0123-456789abcdef
                    [result] => Array
                        (
                            [some_data] => example
                        )

                )

        )

)
```
```

--------------------------------

### Get Live Backlinks Count (Node.js)

Source: https://docs.dataforseo.com/v3/backlinks/bulk_backlinks/live

Node.js example for calling the Bulk Backlinks API to get live backlink counts. This script uses the 'request' module to handle the HTTP POST request.

```javascript
const request = require('request');

const options = {
  url: 'https://api.dataforseo.com/v3/backlinks/bulk_backlinks/live',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + Buffer.from('your_login:your_password').toString('base64') // Replace with your credentials
  },
  body: JSON.stringify({
    targets: [
      "forbes.com",
      "cnn.com",
      "bbc.com",
      "yelp.com",
      "https://www.apple.com/iphone/",
      "https://ahrefs.com/blog/",
      "ibm.com",
      "https://variety.com/",
      "https://stackoverflow.com/",
      "www.trustpilot.com"
    ],
    tag: 'my_task_01'
  })
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);
  console.log(body);
});

```

--------------------------------

### Node.js: Fetch Ready AI Optimization Tasks

Source: https://docs.dataforseo.com/v3/ai_optimization/gemini/llm_responses/tasks_ready

This Node.js example utilizes the `axios` library to make a GET request to the DataForSEO API for ready AI optimization tasks. It demonstrates how to set up authentication using the `auth` object and handle both successful responses and errors.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/ai_optimization/gemini/llm_responses/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch Referring Domains Data with Python

Source: https://docs.dataforseo.com/v3/backlinks/referring_domains/live

This Python snippet shows the initial setup for using the RestClient to access the DataForSEO API. It imports the RestClient and prepares a dictionary for POST data, indicating the start of a request for referring domains.

```python
from client import RestClient
# You can download this file from here https://api.dataforseo.com/v3/_examples/python/_python_Client.zip
client = RestClient("login", "password")
post_data = dict()

```

--------------------------------

### Python Client Example

Source: https://docs.dataforseo.com/v3/keywords_data/google/search_volume/task_get

Example of using the Python client to fetch a list of completed tasks from the DataForSEO API.

```APIDOC
## Python Client Example

### Description
This example demonstrates how to initialize the Python client and fetch a list of completed tasks using the `tasks_ready` endpoint of the DataForSEO API.

### Method
GET

### Endpoint
/v3/keywords_data/google/search_volume/tasks_ready

### Parameters
- **login** (string) - Your DataForSEO API login.
- **password** (string) - Your DataForSEO API password.

### Request Example
```python
from client import RestClient

client = RestClient("login", "password")

response = client.get("/v3/keywords_data/google/search_volume/tasks_ready")

# The response object will contain the list of completed tasks
print(response)
```

### Response
#### Success Response (200)
- **tasks** (array) - A list of completed tasks, each with its own ID and status.

#### Response Example
```json
{
  "status_code": 20000,
  "tasks": [
    {
      "id": "example-task-id",
      "status": "completed",
      "result": [
        {
          "endpoint": "/v3/keywords_data/google/search_volume/task_get/example-task-id"
        }
      ]
    }
  ]
}
```
```

--------------------------------

### Node.js: Get Google Ads Keywords for Site Tasks Ready

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/tasks_ready_php=

This Node.js example uses the 'axios' library to make a GET request to the DataForSEO API for retrieving Google Ads keywords data. It demonstrates setting up basic authentication and content type headers. The result, if successful, is logged to the console.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get Content Analysis Categories via Python

Source: https://docs.dataforseo.com/v3/content_analysis/categories

This Python script utilizes the RestClient to fetch the list of categories from the Content Analysis API. It shows a basic example of making the GET request and receiving the response.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# using this method you can get a list of categories
# GET /v3/content_analysis/categories
response = client.get("/v3/content_analysis/categories")

```

--------------------------------

### Search Business Listings with Node.js

Source: https://docs.dataforseo.com/v3/business_data/business_listings/search/live

This Node.js example uses the 'axios' library to send a POST request to the DataforSEO Business Listings API. It demonstrates how to configure authentication using basic auth, set the request body with search parameters, and handle the response and errors. Replace 'login' and 'password' with your API credentials.

```javascript
const post_array = [];



post_array.push({

    "categories": [

      "pizza_restaurant"

    ],

    "description": "pizza",

    "title": "pizza",

    "is_claimed": true,

    "location_coordinate": "53.476225,-2.243572,10",

    "order_by": [

      "rating.value,desc"

    ],

    "filters": [

      [

        "rating.value",

        ">",

        3

      ]

    ],

    "limit": 3

  });



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/business_data/business_listings/search/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});

```

--------------------------------

### Generate Meta Tags using Node.js (axios)

Source: https://docs.dataforseo.com/v3/content_generation/generate_meta_tags/live

This JavaScript example uses the `axios` library to make a POST request to the DataForSEO API for generating meta tags. It demonstrates setting up the request URL, authentication, payload, and headers. Error handling is also included. Ensure you have `axios` installed (`npm install axios`).

```javascript
const post_array = [];



post_array.push({

        "text": "The idea to develop an instrument for local SEO didn’t come to the GMB Crush CEO, Matteo Barletta, out of the blue. Having a huge interest in search engine optimization, Matteo has come a long way from being an SEO freelancer to launching his own agency, SEO Heroes. At some point, he and his team noticed that it was quite challenging to work with local SEO projects, especially those related to Google My Business listings. There were simply no tools that could streamline their work and provide the functionality the agency needed.nn“We started to develop the idea of ··our tool capable of doing Google Business SEO audits, tracking stats, and generating business proposals at the same time.",

        "creativity": 0.9

});



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/content_generation/generate_meta_tags/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Post Google Hotel Info Task via JavaScript (Node.js)

Source: https://docs.dataforseo.com/v3/business_data/google/hotel_info/task_post

This JavaScript example uses the `axios` library to send POST requests to the Google Hotel Info API. It demonstrates how to set up authentication with `username` and `password`, construct the request body, and handle the response or errors. Ensure you have `axios` installed (`npm install axios`).

```javascript
const post_array = [];



post_array.push({

  "location_name": "New York,New York,United States",

  "language_name": "English",

  "hotel_identifier": encodeURI("ChYIq6SB--i6p6cpGgovbS8wN2s5ODZfEAE", "UTF-8"),

  "priority": 2,

  "tag": "some_string_123",

  "pingback_url": 'https://your-server.com/pingscript?id=$id&tag=$tag'

});



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/business_data/google/hotel_info/task_post',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Set Task with Location Name, Language Name, Keyword, Priority, and Pingback (Python)

Source: https://docs.dataforseo.com/v3/serp/google/organic/task_post

This example shows how to set a task with more detailed parameters, including language and location names, a specific keyword, a priority level for faster processing, and a pingback URL for receiving task completion notifications with dynamic parameters.

```python
post_data = []
post_data.append(dict(
    language_name="English",
    location_name="United States",
    keyword="albert einstein",
    priority=2,
    tag="some_string_123",
    pingback_url="https://your-server.com/pingscript?id=$id&tag=$tag"
))
```

--------------------------------

### GET /v3/keywords_data/bing/locations

Source: https://docs.dataforseo.com/v3/keywords_data/bing/locations_bash=

This endpoint retrieves a list of available locations for keyword data analysis. It supports various search engines, with 'bing' being the default example.

```APIDOC
## GET /v3/keywords_data/bing/locations

### Description
Retrieves a list of locations for keyword data analysis. You can specify other search engines besides 'bing'.

### Method
GET

### Endpoint
/v3/keywords_data/bing/locations

### Parameters

#### Query Parameters

*   **search_engine** (string, optional) - The search engine for which to retrieve locations. Defaults to 'bing'.
*   **other_parameters** (object, optional) - Additional parameters specific to the search engine and data type.

### Request Example
```
GET https://api.dataforseo.com/v3/keywords_data/bing/locations
```

### Response

#### Success Response (20000)

*   **status_code** (integer) - Indicates a successful request.
*   **status_message** (string) - A message indicating the success of the request.
*   **time_taken** (integer) - The time taken to process the request in milliseconds.
*   **data** (object) - Contains the location data.

#### Response Example
```json
{
  "status_code": 20000,
  "status_message": "ok",
  "time_taken": 13,
  "data": {
    "locations": [
      { "location_code": 2854, "location_name": "United States" },
      { "location_code": 2788, "location_name": "United Kingdom" },
      { "location_code": 2772, "location_name": "Germany" }
    ]
  }
}
```

#### Error Response

*   **status_code** (integer) - Indicates an error. Refer to the error codes documentation for details.
*   **status_message** (string) - A message describing the error.
*   **time_taken** (integer) - The time taken to process the request in milliseconds.

#### Error Response Example
```json
{
  "status_code": 40021,
  "status_message": "invalid parameter",
  "time_taken": 4,
  "data": {
    "error_message": "invalid value for parameter $search_engine: example.com"
  }
}
```

### Further Information

For a full list of response codes, please visit: https://docs.dataforseo.com/v3/appendix/errors
```

--------------------------------

### C# DataForSEO API Request Example

Source: https://docs.dataforseo.com/v3/keywords_data/bing/search_volume/tasks_ready_php=

This C# code demonstrates how to set up an HttpClient for the DataForSEO API, including setting the base address and authorization header using basic authentication. It makes a GET request to the '/v3/keywords_data/bing/search_volume/tasks_ready' endpoint, deserializes the JSON response, and checks the 'status_code' for success or failure, printing appropriate messages to the console.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };



            // using this method you can get a list of completed tasks

            // GET /v3/keywords_data/bing/search_volume/tasks_ready

            // in addition to 'search_volume' you can also set other parameters

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/keywords_data/bing/search_volume/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());



            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}
```

--------------------------------

### C#: Fetch Domain Technologies Live Data from DataForSEO API

Source: https://docs.dataforseo.com/v3/domain_analytics/technologies/domain_technologies/live

This C# example demonstrates how to use the DataForSEO API to fetch live domain technologies data. It includes setting up an HttpClient with authentication, sending a POST request to the relevant endpoint, and deserializing the JSON response. Error handling is included to report non-20000 status codes.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task domain_analytics_technologies_domain_technologies_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            // You can set only one task at a time

            postData.Add(new

            {

                target = "dataforseo.com"

            });

            // POST /v3/domain_analytics/technologies/domain_technologies/live

            var taskPostResponse = await httpClient.PostAsync("/v3/domain_analytics/technologies/domain_technologies/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### GET /v2/cmn_user

Source: https://docs.dataforseo.com/v2/cmn_java=

Retrieves user information. This endpoint allows you to fetch details about your Dataforseo account.

```APIDOC
## GET /v2/cmn_user

### Description
Retrieves user information. This endpoint allows you to fetch details about your Dataforseo account.

### Method
GET

### Endpoint
/v2/cmn_user

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
None

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the request. Possible values are "ok" or "error".
- **results** (array) - An array containing the user data if the request is successful.
  - **user_expenses** (object) - Contains information about user expenses.
    - **total_expenses** (integer) - Total expenses incurred.
    - **available_usd** (integer) - Available balance in USD.
  - **user_metrics** (object) - Contains user-specific metrics.
    - **free_max_api_calls** (integer) - Maximum number of free API calls allowed.
    - **api_calls_per_day** (integer) - Number of API calls per day.
    - **api_calls_count** (integer) - Current count of API calls.
    - **used_api_calls** (integer) - Number of API calls used.
    - **free_api_calls_left** (integer) - Remaining free API calls.
    - **free_api_calls_left_date** (string) - Expiration date for free API calls.
    - **paid_api_calls_left** (integer) - Remaining paid API calls.
    - **paid_api_calls_left_date** (string) - Expiration date for paid API calls.
    - **api_calls_monthly_limit** (integer) - Monthly limit for API calls.
    - **api_calls_monthly_limit_date** (string) - Date when the monthly limit resets.

#### Response Example
```json
{
  "status": "ok",
  "results": [
    {
      "user_expenses": {
        "total_expenses": 150,
        "available_usd": 850
      },
      "user_metrics": {
        "free_max_api_calls": 10000,
        "api_calls_per_day": 1000,
        "api_calls_count": 500,
        "used_api_calls": 500,
        "free_api_calls_left": 9500,
        "free_api_calls_left_date": "2024-12-31",
        "paid_api_calls_left": 5000,
        "paid_api_calls_left_date": "2024-12-31",
        "api_calls_monthly_limit": 100000,
        "api_calls_monthly_limit_date": "2024-11-30"
      }
    }
  ]
}
```

### Error Handling
- **error** (object) - Returned if the request fails.
  - **code** (integer) - The error code.
  - **message** (string) - A description of the error.

#### Error Response Example
```json
{
  "status": "error",
  "error": {
    "code": 1002,
    "message": "invalid api key"
  }
}
```
```

--------------------------------

### Fetch Google Relevant Pages Live using Dataforseo API (C#)

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/relevant_pages/live

This C# example demonstrates how to use the Dataforseo API to get relevant pages on Google. It configures an HttpClient with authentication, sets up POST data including target, location, language, filters, and limit, then sends the request and processes the JSON response, handling success and errors.

```C#
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_google_relevant_pages_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(

                new

                {

                    target = "dataforseo.com",

                    location_name = "United States",

                    language_name = "English",

                    filters = new object[]

                    {

                        new object[] { "metrics.organic.pos_1", "<>", 0 },

                        "or",

                        new object[] { "metrics.organic.pos_2_3", "<>", 0 }

                    },

                    limit = 3

                }

            );

            // POST /v3/dataforseo_labs/google/relevant_pages/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/google/relevant_pages/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### GET /v2/cmn_se

Source: https://docs.dataforseo.com/v2/cmn_python=

Retrieves common search engine data. This endpoint is used to fetch information related to search engines.

```APIDOC
## GET /v2/cmn_se

### Description
Retrieves common search engine data. This endpoint is used to fetch information related to search engines.

### Method
GET

### Endpoint
https://api.dataforseo.com/v2/cmn_se

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
None

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the API request. Possible values are 'ok' or 'error'.
- **results** (array) - An array containing the search engine data.

#### Response Example
{
  "status": "ok",
  "results": [
    "google",
    "bing",
    "yahoo"
  ]
}

### Error Handling
- **status** (string) - 'error'
- **error** (object)
  - **code** (integer) - The error code.
  - **message** (string) - A message describing the error.

#### Error Response Example
{
  "status": "error",
  "error": {
    "code": 500,
    "message": "Internal Server Error"
  }
}
```

--------------------------------

### C#: Get Google Ads Status using DataForSEO API

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/status

This C# example demonstrates how to call the DataForSEO '/v3/keywords_data/google_ads/status' endpoint. It sets up an HttpClient with basic authentication, makes a GET request, deserializes the JSON response using Newtonsoft.Json, and then checks the 'status_code' to either print the result or an error message.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_google_ads_status()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };



            // using this method you can get a list of endpoints

            // GET /v3/keywords_data/google_ads/status

            var response = await httpClient.GetAsync("/v3/keywords_data/google_ads/status");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Example Place Topics Structure

Source: https://docs.dataforseo.com/v3/business_data/business_listings/search/live

Demonstrates the structure for 'place_topics', which lists keywords from customer reviews and the count of reviews mentioning each keyword. This helps in understanding the most popular topics related to a business's products or services.

```json
{
  "place_topics": {
    "egg roll": 48,
    "birthday": 33
  }
}
```

--------------------------------

### JavaScript (Node.js): Authenticate and GET SERP tasks

Source: https://docs.dataforseo.com/v3/serp/baidu/organic/tasks_fixed

This Node.js example uses the `axios` library to make an authenticated GET request to the DataForSEO API for Baidu organic search tasks. It handles successful responses by logging the task result and errors by logging the error object.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/baidu/organic/tasks_fixed',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### DataforSEO API Access Example (Node.js)

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live

This Node.js example illustrates making authenticated API calls to DataforSEO. It requires setting up authorization headers with your API credentials. This snippet is useful for backend integrations.

```javascript
const https = require('https');

const options = {
    hostname: 'api.dataforseo.com',
    port: 443,
    path: '/v3/...',
    method: 'GET',
    headers: {
        'Authorization': 'Basic ' + Buffer.from('login:password').toString('base64')
    }
};

const req = https.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => {
        data += chunk;
    });
    res.on('end', () => {
        console.log(JSON.parse(data));
    });
});

req.on('error', (e) => {
    console.error(`problem with request: ${e.message}`);
});

req.end();
```

--------------------------------

### Fetch Amazon Product Tasks Ready with PHP

Source: https://docs.dataforseo.com/v3/merchant/amazon/products/tasks_ready

This PHP example demonstrates how to fetch a list of completed tasks for Amazon products using the provided RestClient. It requires downloading the `php_RestClient.zip` and including `RestClient.php`. The code initializes the client with API credentials and calls the `get` method for the relevant endpoint. Error handling for API requests is included.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');



try {

   // using this method you can get a list of completed tasks

   // GET /v3/merchant/amazon/products/tasks_ready

   $result = $client->get('/v3/merchant/amazon/products/tasks_ready');

   print_r($result);

   // do something with result

} catch (RestClientException $e) {

   echo "n";

   print "HTTP code: {$e->getHttpCode()}n";

   print "Error code: {$e->getCode()}n";

   print "Message: {$e->getMessage()}n";

   print  $e->getTraceAsString();

   echo "n";

}

$client = null;

?>
```

--------------------------------

### Node.js: Get SERP Seznam Organic Task Results

Source: https://docs.dataforseo.com/v3/serp/seznam/organic/task_get/advanced

Example using Axios in Node.js to fetch completed organic search task results from Seznam.

```APIDOC
## Node.js Example

### Description
This Node.js script uses the Axios library to make a GET request to retrieve the results of a completed organic search task for Seznam.

### Method
GET

### Endpoint
`/v3/serp/seznam/organic/task_get/advanced/${task_id}`

### Parameters
#### Path Parameters
- **task_id** (string) - Required - The unique identifier of the completed task.

### Request Example
```javascript
const axios = require('axios');

const taskId = 'your_task_id'; // Replace with your actual task ID

axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/serp/seznam/organic/task_get/advanced/' + taskId,
    auth: {
        username: 'your_login', // Replace with your login
        password: 'your_password'  // Replace with your password
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response.data.tasks;
    // Process the result data
    console.log(result);
}).catch(function (error) {
    console.error('Error fetching task results:', error);
});
```
```

--------------------------------

### GET /v3/serp/google/ads_search/tasks_ready (cURL)

Source: https://docs.dataforseo.com/v3/serp/google/ads_search/tasks_ready_php=

This example demonstrates how to retrieve a list of completed tasks from the DataForSEO API using cURL. It includes authentication using a base64 encoded login and password.

```APIDOC
## GET /v3/serp/google/ads_search/tasks_ready

### Description
Retrieves a list of completed tasks for Google Ads search.

### Method
GET

### Endpoint
https://api.dataforseo.com/v3/serp/google/ads_search/tasks_ready

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```bash
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"

curl --location --request GET "https://api.dataforseo.com/v3/serp/google/ads_search/tasks_ready" \
--header "Authorization: Basic ${cred}" \
--header "Content-Type: application/json" \
--data-raw ""
```

### Response
#### Success Response (200)
- **tasks** (array) - An array of completed tasks.
  - **id** (string) - The ID of the task.
  - **result** (object) - The result of the task.

#### Response Example
```json
{
    "tasks": [
        {
            "id": "01234567-89ab-cdef-0123-456789abcdef",
            "result": {
                "some_data": "example"
            }
        }
    ]
}
```
```

--------------------------------

### PHP: Get SERP Seznam Organic Task Results

Source: https://docs.dataforseo.com/v3/serp/seznam/organic/task_get/advanced

Example using the RestClient in PHP to fetch completed organic search task results from Seznam.

```APIDOC
## PHP Example

### Description
This PHP script demonstrates how to use the `RestClient` class to retrieve a list of completed tasks and their results for Seznam organic search.

### Method
GET

### Endpoint
`/v3/serp/seznam/organic/tasks_ready` and `/v3/serp/seznam/organic/task_get/advanced/$id`

### Parameters
(See general API documentation for parameter details)

### Request Example
```php
<?php

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {
  // Replace 'login' and 'password' with your actual credentials
  $client = new RestClient($api_url, null, 'login', 'password');
} catch (RestClientException $e) {
  // Handle exceptions
  echo "nHTTP code: {$e->getHttpCode()}n";
  print "Error code: {$e->getCode()}n";
  print "Message: {$e->getMessage()}n";
  exit();
}

try {
  $result = array();

  // Get a list of completed tasks
  $tasks_ready = $client->get('/v3/serp/seznam/organic/tasks_ready');

  if (isset($tasks_ready['status_code']) && $tasks_ready['status_code'] === 20000 && isset($tasks_ready['tasks'])) {
    foreach ($tasks_ready['tasks'] as $task) {
      if (isset($task['result'])) {
        foreach ($task['result'] as $task_ready) {
          // Get results of each completed task using endpoint_advanced
          if (isset($task_ready['endpoint_advanced'])) {
            $result[] = $client->get($task_ready['endpoint_advanced']);
          }
          // Alternatively, get results by task ID
          /*
          if (isset($task_ready['id'])) {
            $result[] = $client->get('/v3/serp/seznam/organic/task_get/advanced/' . $task_ready['id']);
          }
          */
        }
      }
    }
  }
  print_r($result);

} catch (RestClientException $e) {
  // Handle exceptions
  echo "nHTTP code: {$e->getHttpCode()}n";
  print "Error code: {$e->getCode()}n";
  print "Message: {$e->getMessage()}n";
}

$client = null;

?>
```
```

--------------------------------

### GET /v2/cmn_user

Source: https://docs.dataforseo.com/v2/cmn_java=

Retrieves the user's account information, including balance, credits, and rate limits.

```APIDOC
## GET /v2/cmn_user

### Description
This endpoint retrieves the user's account information, including their current balance, available credits, and API rate limits.

### Method
GET

### Endpoint
https://api.dataforseo.com/v2/cmn_user

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```bash
curl -X GET "https://api.dataforseo.com/v2/cmn_user" \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic YOUR_BASE64_ENCODED_CREDENTIALS"
```

### Response
#### Success Response (200)
- **status** (string) - The status of the request, e.g., "ok".
- **results_time** (string) - The time taken to process the request.
- **results_count** (integer) - The number of results returned.
- **results** (array) - An array containing user account details.
  - **login** (string) - User's login.
  - **timezone** (string) - User's timezone.
  - **rate_limit_per_minute** (integer) - The number of requests allowed per minute.
  - **rate** (integer) - The current rate.
  - **rate_max** (integer) - The maximum rate.
  - **credit** (integer) - The number of available credits.
  - **balance** (float) - The user's account balance.
  - **count_total** (float) - Total count of tasks.
  - **count_rnk** (integer) - Count of rank tracking tasks.
  - **count_srp** (float) - Count of SERP tasks.
  - **count_kwrd** (integer) - Count of keyword tasks.
  - **count_pg** (integer) - Count of page tasks.
  - **count_cmp** (integer) - Count of competitor tasks.
  - **price** (object) - Pricing information for different API services.

#### Response Example
```json
{
    "status": "ok",
    "results_time": "0.0173 sec.",
    "results_count": 1,
    "results": [
        {
            "login": "superlogin",
            "timezone": "Europe/London",
            "rate_limit_per_minute": 1000,
            "rate": 1,
            "rate_max": 123,
            "credit": 99999999,
            "balance": 99987531.5,
            "count_total": 12467.5,
            "count_rnk": 1466,
            "count_srp": 9149.5,
            "count_kwrd": 3047,
            "count_pg": 0,
            "count_cmp": 0,
            "price": {
                "apiRnk": {
                    "rnk_tasks_post": {
                        "priority_low": {
                            "price_type": "per_result",
                            "price": 1
                        },
                        "priority_normal": {
                            "price_type": "per_result",
                            "price": 1
                        },
                        "priority_high": {
                            "price_type": "per_result",
                            "price": 2
                        },
                        "priority_vip": {
                            "price_type": "per_result",
                            "price": 5
                        }
                    }
                },
                "apiSrp": {
                    "srp_tasks_post": {
                        "priority_low": {
                            "price_type": "per_result",
                            "price": 0
                        },
                        "priority_normal": {
                            "price_type": "per_result",
                            "price": 0
                        },
                        "priority_high": {
                            "price_type": "per_result",
                            "price": 2
                        },
                        "priority_vip": {
                            "price_type": "per_result",
                            "price": 5
                        }
                    },
                    "srp_100": {
                        "priority_low": {
                            "price_type": "per_request",
                            "price": 1
                        },
                        "priority_normal": {
                            "price_type": "per_request",
                            "price": 1
                        },
                        "priority_high": {
                            "price_type": "per_request",
                            "price": 1
                        },
                        "priority_vip": {
                            "price_type": "per_request",
                            "price": 1
                        }
                    }
                }
            }
        }
    ]
}

#### Error Response (4xx or 5xx)
- **status** (string) - The status of the request, e.g., "error".
- **error** (object) - An object containing error details.
  - **code** (integer) - The error code.
  - **message** (string) - A description of the error.

#### Error Response Example
```json
{
    "status": "error",
    "error": {
        "code": 401,
        "message": "Authorization error. Please check your credentials."
    }
}
```
```

--------------------------------

### Fetch Google Finance Explore Tasks Ready using Bash

Source: https://docs.dataforseo.com/v3/serp/google/finance_explore/tasks_ready

This snippet shows how to make a GET request to the 'serp/google/finance_explore/tasks_ready' endpoint using curl in Bash. It includes basic authentication and header setup. Ensure you replace 'login' and 'password' with your actual API credentials.

```bash
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"

curl --location --request GET "https://api.dataforseo.com/v3/serp/google/finance_explore/tasks_ready" \
--header "Authorization: Basic ${cred}" \
--header "Content-Type: application/json" \
--data-raw ""
```

--------------------------------

### GET /v2/cmn_se

Source: https://docs.dataforseo.com/v2/cmn_java=

This endpoint retrieves a list of supported search engines. It requires API credentials for authentication.

```APIDOC
## GET /v2/cmn_se

### Description
Retrieves a list of supported search engines.

### Method
GET

### Endpoint
/v2/cmn_se

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```php
<?php
require('RestClient.php');
//You can download this file from here https://api.dataforseo.com/_examples/php/_php_RestClient.zip
try {
    //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
    $client = new RestClient('https://api.dataforseo.com/', null, 'login', 'password');
    $se_get_result = $client->get('v2/cmn_se');
    print_r($se_get_result);
    //do something with se
} catch (RestClientException $e) {
    echo "\n";
    print "HTTP code: {$e->getHttpCode()}\n";
    print "Error code: {$e->getCode()}\n";
    print "Message: {$e->getMessage()}\n";
    print  $e->getTraceAsString();
    echo "\n";
    exit();
}
$client = null;
?>
```

```python
from client import RestClient
#You can download this file from here https://api.dataforseo.com/_examples/php/_php_RestClient.zip
#Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
client = RestClient("login", "password")
response = client.get("/v2/cmn_se")
if response["status"] == "error":
    print("error. Code: %d Message: %s" % (response["error"]["code"], response["error"]["message"]))
else:
    print(response["results"])
```

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task cmn_se()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };
            var response = await httpClient.GetAsync("v2/cmn_se");
            var obj = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());
            if (obj.status == "error")
                Console.WriteLine($"error. Code: {obj.error.code} Message: {obj.error.message}");
            else
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the request ('ok' or 'error').
- **error** (object) - Contains error details if the status is 'error'.
  - **code** (integer) - Error code.
  - **message** (string) - Error message.
- **results** (array) - An array of search engine objects if the request is successful.
  - **id** (integer) - The unique identifier for the search engine.
  - **name** (string) - The name of the search engine.
  - **countries** (array) - A list of country codes where the search engine is available.

#### Response Example
```json
{
  "status": "ok",
  "results": [
    {
      "id": 1,
      "name": "google",
      "countries": ["us", "gb", "de", ...]
    },
    {
      "id": 2,
      "name": "bing",
      "countries": ["us", "gb", "de", ...]
    }
  ]
}
```
```

--------------------------------

### Fetch Google Finance Explore Tasks Ready using PHP

Source: https://docs.dataforseo.com/v3/serp/google/finance_explore/tasks_ready

This PHP example demonstrates how to use the provided RestClient to fetch data from the 'serp/google/finance_explore/tasks_ready' endpoint. It includes error handling for API requests and requires the RestClient.php file. Remember to replace placeholder credentials.

```php
require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {
    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
    $client = new RestClient($api_url, null, 'login', 'password');
} catch (RestClientException $e) {
    echo "\n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "\n";
    exit();
}

try {
    // using this method you can get a list of completed tasks
    // GET /v3/serp/google/finance_explore/tasks_ready
    // in addition to 'google' and 'finance_explore' you can also set other search engine and type parameters
    // the full list of possible parameters is available in documentation
    $result = $client->get('/v3/serp/google/finance_explore/tasks_ready');
    print_r($result);
    // do something with result
} catch (RestClientException $e) {
    echo "\n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "\n";
}

$client = null;
```

--------------------------------

### Sandbox POST Request Example

Source: https://docs.dataforseo.com/v3/app_data/google/overview

This example demonstrates how to make a POST request to a sandbox endpoint. The primary change is replacing the production hostname with the sandbox hostname.

```APIDOC
## POST /v3/$path

### Description
This endpoint allows sending POST requests to sandbox API endpoints. Replace `$path` with the specific API path you wish to test.

### Method
POST

### Endpoint
https://sandbox.dataforseo.com/v3/$path

### Parameters
#### Path Parameters
- **path** (string) - Required - The API path to the endpoint you’d like to test (e.g., `_serp/google/maps/task_post_`).

### Request Example
```json
{
  "path": "_serp/google/maps/task_post_"
}
```

### Response
#### Success Response (200)
- **status** (string) - The status of the request.
- **data** (object) - The response data from the sandbox API, containing dummy data.

#### Response Example
```json
{
  "status": "ok",
  "data": {
    "keyword": "example_keyword",
    "placeholder_field": "dummy_data"
  }
}
```
```

--------------------------------

### Authenticate and Get Google Hotel Info Tasks Ready (PHP)

Source: https://docs.dataforseo.com/v3/business_data/google/hotel_info/tasks_ready

This PHP example demonstrates how to use the provided `RestClient` class to authenticate with the DataForSEO API and retrieve a list of completed tasks for Google Hotel Info. It includes error handling for `RestClientException`.

```php
<?php

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');



try {

    $result = array();

    // #1 - using this method you can get a list of completed tasks

    // GET /v3/business_data/google/hotel_info/tasks_ready

    $result = $client->get('/v3/business_data/google/hotel_info/tasks_ready');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### C#: Fetch Google App Metrics in Bulk

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/bulk_app_metrics/live

This C# example shows how to use the DataForSEO Labs Google Bulk App Metrics Live API. It configures an HttpClient with authentication, prepares a list of app metrics requests, sends a POST request, and deserializes the JSON response to check for success or errors.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_google_bulk_app_metrics_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                app_ids = [

                "org.telegram.messenger",

                "com.zhiliaoapp.musically"

                ],

                location_name = "United States",

                language_name = "English"

            });

            // POST /v3/dataforseo_labs/google/bulk_app_metrics/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/google/bulk_app_metrics/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### GET /v2/cmn_key_id/{keyword}

Source: https://docs.dataforseo.com/v2/cmn_csharp=

Retrieves the key_id for a given keyword from the DataForSEO database. If the keyword does not exist, it will be added and a new key_id will be generated.

```APIDOC
## GET /v2/cmn_key_id/{keyword}

### Description
This endpoint allows you to obtain the unique key_id for a specified keyword. If the keyword is not found in the database, it will be automatically added, and a new key_id will be generated and returned. This key_id can then be used with other DataForSEO APIs, such as the Rank Tracker API and SERP API. The key_id is permanent and cannot be altered.

### Method
GET

### Endpoint
`https://api.dataforseo.com/v2/cmn_key_id/$keyword`

### Parameters
#### Path Parameters
- **keyword** (string) - Required - The keyword for which to retrieve or create a key_id.

### Request Example
```bash
curl -X GET https://api.dataforseo.com/v2/cmn_key_id/online%20rank%20checker \
     -H "Authorization: Basic YOUR_BASIC_AUTH_STRING"
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the operation. Possible values are "ok" or "error".
- **results_time** (string) - The time taken for the API request to complete, in seconds.
- **results_count** (string) - The number of results returned in the `results` array.
- **results** (array) - An array containing keyword IDs.
  - **key_id** (integer) - The unique identifier for the keyword.

#### Error Response
- **status** (string) - "error"
- **error** (array) - An array containing error details.
  - **code** (integer) - The error code.
  - **message** (string) - A text description of the error.

#### Response Example
```json
{
    "status": "ok",
    "results_time": "0.0115 sec.",
    "results_count": 1,
    "results": [
        {
            "key_id": 1095202
        }
    ]
}
```
```

--------------------------------

### Fetch YouTube Organic Tasks Ready (JavaScript/Node.js)

Source: https://docs.dataforseo.com/v3/serp/youtube/organic/tasks_ready

This Node.js example uses the 'axios' library to make a GET request to the DataForSEO API. It demonstrates how to configure the request with basic authentication and headers to fetch completed tasks from the /v3/serp/youtube/organic/tasks_ready endpoint.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/youtube/organic/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});

```

--------------------------------

### DataForSEO API Request Examples

Source: https://docs.dataforseo.com/v3/serp/yahoo/organic/live/html

Provides example code for making requests to the DataForSEO API. These examples demonstrate how to authenticate and structure requests using different programming languages. Replace 'login' and 'password' with your actual API credentials.

```bash
curl -X POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \
-H "Content-Type: application/json" \
-u "login:password" \
-d 
'{ 
  "task_settings": {
    "max_crawl_pages": 10
  },
  "data": [
    {
      "keyword": "example",
      "location_code": 2888,
      "language_code": "en"
    }
  ]
}'
```

```php
<?php
    $curl = curl_init();

    curl_setopt($curl, CURLOPT_URL, "https://api.dataforseo.com/v3/serp/google/organic/live/advanced");
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_POST, 1);
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode(array(
        "task_settings" => array(
            "max_crawl_pages" => 10
        ),
        "data" => array(
            array(
                "keyword" => "example",
                "location_code" => 2888,
                "language_code" => "en"
            )
        )
    )));

    $headers = array();
    $headers[] = "Content-Type: application/json";
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

    // Replace login:password with your credentials
    curl_setopt($curl, CURLOPT_USERPWD, "login:password");

    $result = curl_exec($curl);
    if (curl_errno($curl)) {
        echo 'Error:' . curl_error($curl);
    }
    curl_close($curl);

    echo ($result);
?>
```

```javascript
const https = require('https');

const options = {
    hostname: 'api.dataforseo.com',
    port: 443,
    path: '/v3/serp/google/organic/live/advanced',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + Buffer.from('login:password').toString('base64') // Replace login:password with your credentials
    }
};

const req = https.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => {
        data += chunk;
    });
    res.on('end', () => {
        console.log(JSON.parse(data));
    });
});

req.on('error', (error) => {
    console.error(error);
});

const postData = JSON.stringify({
    "task_settings": {
        "max_crawl_pages": 10
    },
    "data": [
        {
            "keyword": "example",
            "location_code": 2888,
            "language_code": "en"
        }
    ]
});

req.write(postData);
req.end();
```

```python
import requests
import json

api_url = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
auth = ('login', 'password') # Replace login:password with your credentials

headers = {
    "Content-Type": "application/json"
}

payload = {
    "task_settings": {
        "max_crawl_pages": 10
    },
    "data": [
        {
            "keyword": "example",
            "location_code": 2888,
            "language_code": "en"
        }
    ]
}

response = requests.post(api_url, auth=auth, headers=headers, data=json.dumps(payload))

print(response.json())

```

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

public class DataForSeoClient
{
    public static async Task MakeRequestAsync()
    {
        using (var httpClient = new HttpClient())
        {
            // Replace login:password with your credentials
            var authToken = Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"));
            httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", authToken);

            var requestBody = new
            {
                task_settings = new
                {
                    max_crawl_pages = 10
                },
                data = new object[]
                {
                    new
                    {
                        keyword = "example",
                        location_code = 2888,
                        language_code = "en"
                    }
                }
            };

            var jsonPayload = System.Text.Json.JsonSerializer.Serialize(requestBody);

            var response = await httpClient.PostAsync("https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
                new StringContent(jsonPayload, Encoding.UTF8, "application/json"));

            var responseContent = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseContent);
        }
    }

    public static void Main(string[] args)
    {
        MakeRequestAsync().Wait();
    }
}
```

--------------------------------

### GET /v2/op_tasks_get_duplicates/{task_id}

Source: https://docs.dataforseo.com/v2/op_java=

Retrieves duplicate tasks associated with a given task ID. Includes authentication setup and response handling for success and error cases.

```APIDOC
## GET /v2/op_tasks_get_duplicates/{task_id}

### Description
This endpoint retrieves duplicate tasks for a specified task ID. It handles authentication using Basic HTTP Authentication and deserializes the JSON response to check for errors or display results.

### Method
GET

### Endpoint
`https://api.dataforseo.com/v2/op_tasks_get_duplicates/{task_id}`

### Parameters
#### Path Parameters
- **task_id** (integer) - Required - The ID of the task to retrieve duplicates for.

#### Query Parameters
None

#### Request Body
None

### Request Example
(No request body is sent for this GET request. Authentication is typically handled via headers.)

### Response
#### Success Response (200)
- **status** (string) - The status of the operation ('ok' or 'error').
- **results_count** (integer) - The number of results found.
- **results** (array) - An array of duplicate task results.
- **error** (object) - Contains error code and message if status is 'error'.
  - **code** (integer) - Error code.
  - **message** (string) - Error message.

#### Response Example
```json
{
  "status": "ok",
  "results_count": 2,
  "results": [
    {
      "domain": "example.com",
      "first_seen": "2023-01-15T10:00:00Z",
      "last_seen": "2023-10-20T12:00:00Z"
    },
    {
      "domain": "another.com",
      "first_seen": "2023-02-10T11:00:00Z",
      "last_seen": "2023-11-01T13:00:00Z"
    }
  ]
}
```

#### Error Response Example
```json
{
  "status": "error",
  "error": {
    "code": 404,
    "message": "Task not found"
  }
}
```
```

--------------------------------

### Fetch Keywords for a Site using DataForSEO API (C#)

Source: https://docs.dataforseo.com/v3/keywords_data/bing/keywords_for_site/live

This C# example shows how to make a POST request to the DataForSEO API's '/v3/keywords_data/bing/keywords_for_site/live' endpoint. It uses HttpClient and Newtonsoft.Json for making the request and deserializing the JSON response. The code includes setting up authentication and handling the response, similar to the Python example, checking for a 20000 status code.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_keywords_for_site_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                location_name = "United States",

                language_name = "English",

                target = "dataforseo.com"

            });

            // POST /v3/keywords_data/bing/keywords_for_site/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/keywords_data/bing/keywords_for_site/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}
```

--------------------------------

### DataforSEO API Access Example (Python)

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live

This Python script provides a way to interact with the DataforSEO API, including authentication using your provided credentials. It demonstrates a basic GET request and handling the JSON response.

```python
import requests
from base64 import b64encode

# Instead of ‘login’ and ‘password’ use your credentials from https://app.dataforseo.com/api-access
login = "login"
password = "password"

credentials = f"{login}:{password}"
encoded_credentials = b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_credentials}"
}

response = requests.get("https://api.dataforseo.com/v3/...", headers=headers)

print(response.json())
```

--------------------------------

### PHP: Create Ranking Task using Text Parameters

Source: https://docs.dataforseo.com/v2/rnk_csharp=

This example sets up a ranking task using text-based parameters for search engine, language, and location. It is faster than example #1 but requires more specific input. The API will process these text inputs to determine the internal IDs.

```php
// example #2 - will return results faster than #1, but is simpler than example #3
// All parameters should be set in the text format.
// All data will be will be searched, compared to our internal parameters
// and used as:
// "se_id", "loc_id", "key_id" ( actual and
// fresh list can be found here: "se_id": https://api.dataforseo.com/v2/cmn_se ,
// "loc_id": https://api.dataforseo.com/v2/cmn_locations )
// If a task was set successfully, this *_id will be returned in results: 'v2/rnk_tasks_post' so you can use it.
// The setting of a task can fail, if you set not-existent search engine, for example.
// Disadvantages: The process of search and comparison of provided data to our internal parameters may take some time.
$my_unq_id = mt_rand(0, 30000000); // your unique ID. we will return it with all results. you can set your database ID, string, etc.
$post_array[$my_unq_id] = array(
    "priority" => 1,
    "site" => "dataforseo.com",
    "se_name" => "google.co.uk",
    "se_language" => "English",
    "loc_name_canonical" => "London,England,United Kingdom",
    "key" => mb_convert_encoding("seo data api", "UTF-8")
    //,"pingback_url" => "http://your-domain.com/pingback_url_example.php?task_id=$task_id" //see pingback_url_example.php script
);
```

--------------------------------

### Get App Info Tasks Ready with Bash

Source: https://docs.dataforseo.com/v3/app_data/google/app_info/tasks_ready

This Bash script demonstrates how to fetch a list of completed tasks for app info using the Dataforseo API. It utilizes `curl` for making the HTTP GET request and `base64` for encoding credentials. Ensure you replace 'login' and 'password' with your actual API credentials.

```bash
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"

curl --location --request GET "https://api.dataforseo.com/v3/app_data/google/app_info/tasks_ready" \
--header "Authorization: Basic ${cred}" \
--header "Content-Type: application/json" \
--data-raw ""
```

--------------------------------

### PHP: Authenticate and GET SERP tasks

Source: https://docs.dataforseo.com/v3/serp/baidu/organic/tasks_fixed

This PHP example demonstrates how to authenticate with the DataForSEO API using a provided RestClient class and retrieve a list of completed Baidu organic search tasks. It requires the `RestClient.php` file and handles potential API exceptions.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {

    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

    $client = new RestClient($api_url, null, 'login', 'password');

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

    exit();

}

try {

    // using this method you can get a list of completed tasks

    // GET /v3/serp/baidu/organic/tasks_fixed

    // in addition to 'baidu' and 'organic' you can also set other search engine and type parameters

    // the full list of possible parameters is available in documentation

    $result = $client->get('/v3/serp/baidu/organic/tasks_fixed');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### Fetch Baidu Organic SERP Tasks Ready (JavaScript)

Source: https://docs.dataforseo.com/v3/serp/baidu/organic/tasks_ready

This JavaScript (Node.js) example uses the `axios` library to make an authenticated GET request to the DataForSEO API. It demonstrates how to set up authorization using basic auth and retrieve the results of completed Baidu organic search tasks.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/baidu/organic/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### C#: Make Google Keyword Ideas API Request and Handle Response

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live

This C# example shows how to use the dataforseo API to get Google keyword ideas. It includes setting up the HTTP client, constructing the POST request with parameters, sending the request, and deserializing the JSON response. It then checks the status code and prints the result or an error message.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_google_keyword_ideas_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                keywords = new[]

                {

                    "phone",

                    "watch"

                },

                location_name = "United States",

                language_name = "English",

                filters = new object[]

                {

                    new object[] { "keyword_info.search_volume", ">", 10 }

                },

                limit = 3

            });

            // POST /v3/dataforseo_labs/google/keyword_ideas/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/google/keyword_ideas/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Retrieve Product URL using ad_aclk (Java)

Source: https://docs.dataforseo.com/v2/merchant_python=

Java code example for interacting with the merchant_google_shopping_shops_ad_url endpoint. It shows how to make the GET request and handle the JSON response using libraries like Jackson.

```java
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.List;

public class DataForSEOApiClient {

    private static final HttpClient client = HttpClient.newHttpClient();
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void getProductUrl(String adAclk) throws IOException, InterruptedException {
        String url = "https://api.dataforseo.com/v2/merchant_google_shopping_shops_ad_url/" + adAclk;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() >= 200 && response.statusCode() < 300) {
            try {
                ApiResponse data = objectMapper.readValue(response.body(), ApiResponse.class);
                if (data != null && data.getResults() != null && !data.getResults().isEmpty()) {
                    for (Result result : data.getResults()) {
                        if ("ok".equals(result.getStatus())) {
                            System.out.println("Product URL: " + result.getAi_url());
                        } else {
                            String errorMessage = "Unknown error";
                            if (result.getError() != null && !result.getError().isEmpty()) {
                                errorMessage = result.getError().get(0).getMessage();
                            }
                            System.out.println("Error: " + errorMessage);
                        }
                    }
                } else {
                    System.out.println("No results found or an error occurred.");
                }
            } catch (IOException e) {
                System.err.println("Failed to parse JSON response: " + e.getMessage());
            }
        } else {
            System.err.println("HTTP Request failed with status code: " + response.statusCode());
        }
    }

    // --- POJO Classes for JSON parsing --- 
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class ApiResponse {
        private List<Result> results;

        public List<Result> getResults() { return results; }
        public void setResults(List<Result> results) { this.results = results; }
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Result {
        private String status;
        private List<Error> error;
        private long task_id;
        private String ai_url;

        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        public List<Error> getError() { return error; }
        public void setError(List<Error> error) { this.error = error; }
        public long getTask_id() { return task_id; }
        public void setTask_id(long task_id) { this.task_id = task_id; }
        public String getAi_url() { return ai_url; }
        public void setAi_url(String ai_url) { this.ai_url = ai_url; }
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Error {
        private int code;
        private String message;

        public int getCode() { return code; }
        public void setCode(int code) { this.code = code; }
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
    }

    // Example usage:
    // public static void main(String[] args) {
    //     try {
    //         String adAclk = "YOUR_AD_ACLK_PARAMETER";
    //         getProductUrl(adAclk);
    //     } catch (IOException | InterruptedException e) {
    //         e.printStackTrace();
    //     }
    // }
}
```

--------------------------------

### Fetch Backlink Summary with Python

Source: https://docs.dataforseo.com/v3/backlinks/summary/live

This Python snippet demonstrates how to use the provided `RestClient` to interact with the DataForSEO API. It shows how to initialize the client with credentials, construct the POST data dictionary, and make the request to the backlinks summary live endpoint. The `python_Client.zip` file is required for this example.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    target="explodingtopics.com",
    internal_list_limit=10,
    include_subdomains=True,
    backlinks_filters=["dofollow", "=", True],
    backlinks_status_type="all"
)
# POST /v3/backlinks/summary/live
response = client.post("/v3/backlinks/summary/live", post_data)
```

--------------------------------

### Fetch Data Using Axios in Node.js

Source: https://docs.dataforseo.com/v3/keywords_data/bing/keywords_for_keywords/tasks_ready_php=

This JavaScript snippet uses the Axios library to make a GET request to the Dataforseo API for completed tasks. It handles authentication via the `auth` object and processes the response or logs errors. Ensure Axios is installed (`npm install axios`).

```javascript
const axios = require('axios');

axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/keywords_data/bing/keywords_for_keywords/tasks_ready',
    auth: {
        username: 'login',
        password: 'password'
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response['data']['tasks'][0]['result'];
    // Result data
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

--------------------------------

### Fetch Completed Tasks Using Node.js (Axios)

Source: https://docs.dataforseo.com/v3/app_data/apple/app_searches/tasks_ready

This JavaScript example uses the popular `axios` library to make a GET request to the DataForSEO API. It demonstrates how to set up authentication using `username` and `password` within the request configuration and specifies the `content-type` header. The response data or any errors are logged to the console.

```javascript
const axios = require('axios');

axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/app_data/apple/app_searches/tasks_ready',
    auth: {
        username: 'login',
        password: 'password'
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    // Access the result data from the first task
    var result = response['data']['tasks'][0]['result'];
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

--------------------------------

### Get Google Adwords Status using Node.js (Axios)

Source: https://docs.dataforseo.com/v3/keywords_data/google/adwords_status_php=

This JavaScript example uses the 'axios' library to make an authenticated GET request to the Dataforseo API for retrieving Google Adwords status. It demonstrates setting up the request with authorization credentials and content type headers, and handling the response or errors.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/keywords_data/google/adwords_status',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### C#: Post Google Sellers Task with DataforSEO API

Source: https://docs.dataforseo.com/v3/merchant/google/sellers/task_post_php=

This C# example shows how to interact with the DataforSEO API to post tasks for Google Shopping sellers. It covers setting up an HttpClient with authentication, preparing POST data with various options (basic, with priority, with postback URL), sending the request, and deserializing the JSON response for success or error handling.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task merchant_google_sellers_task_post()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))
                }
            };

            var postData = new List<object>();

            // example #1 - a simple way to set a task

            // this way requires you to specify a location, a language of search, and a product_id.

            postData.Add(new

            {

                location_name = "United States",

                language_name = "English",

                product_id = "1113158713975221117"

            });

            // example #2 - a way to set a task with additional parameters

            // high priority allows us to complete a task faster, but you will be charged more credits.

            // after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.

            postData.Add(new

            {

                location_name = "United States",

                language_name = "English",

                product_id = "1113158713975221117",

                priority = 2,

                tag = "some_string_123",

                pingback_url = "https://your-server.com/pingscript?id=$id&tag=$tag"

            });

            // example #3 - an alternative way to set a task

            // after a task is completed, we will send the results according to the address you set in the 'postback_url' field.

            postData.Add(new

            {

                location_name = "United States",

                language_name = "English",

                product_id = "1113158713975221117",

                postback_data = "html",

                postback_url = "https://your-server.com/postbackscript"

            });

            // POST /v3/merchant/google/sellers/task_post

            var taskPostResponse = await httpClient.PostAsync("/v3/merchant/google/sellers/task_post", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Languages List via Node.js

Source: https://docs.dataforseo.com/v3/content_generation/text_summary/languages

This Node.js example uses the 'axios' library to make a GET request to the API for language lists. It includes basic authentication and sets the necessary headers. The result is logged to the console.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/content_generation/text_summary/languages',

    auth: {

        username: 'login',

        password: 'password'

    },

    data: [{

        version: "v3"

    }],

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get API Errors List using Node.js

Source: https://docs.dataforseo.com/v3/appendix/errors

This Node.js example uses the axios library to make a GET request to the /v3/appendix/errors endpoint. It handles authentication using basic auth and specifies JSON content type. The response data, including results, is logged to the console, along with any errors.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/appendix/errors',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});

```

--------------------------------

### Fetch Amazon Related Keywords (JavaScript/Node.js)

Source: https://docs.dataforseo.com/v3/dataforseo_labs/amazon/related_keywords/live

This Node.js example uses the `axios` library to make a POST request to the DataForSEO API. It demonstrates how to set up the request with basic authentication, headers, and the JSON payload containing the keyword and location details. The example logs the API response or any errors encountered.

```javascript
const post_array = [];



post_array.push({

  "keyword": "computer mouse",

  "language_name": "English",

  "location_code": 2840,

  "limit": 5,

  "include_seed_keyword": true



});



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/dataforseo_labs/amazon/related_keywords/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Initialize DataForSEO Client using Python

Source: https://docs.dataforseo.com/v3/serp/google/local_finder/live/advanced

This Python snippet shows how to initialize the RestClient for the DataForSEO API. It requires your login and password credentials. The `post_data` dictionary is prepared for subsequent API requests. The RestClient zip file needs to be downloaded from the provided URL.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip



client = RestClient("login", "password")
post_data = dict()

```

--------------------------------

### C#: Fetch and Process SERP Google Autocomplete Tasks Ready API

Source: https://docs.dataforseo.com/v3/serp/google/autocomplete/tasks_ready_php=

This C# example demonstrates how to asynchronously fetch data from the DataForSEO SERP Google Autocomplete Tasks Ready API. It includes setting up an HttpClient with authentication, making the GET request, and deserializing the JSON response. Error handling is implemented by checking the status code.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/serp/google/autocomplete/tasks_ready

            // in addition to 'google' and 'autocomplete' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/serp/google/autocomplete/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Fetch Merchant Google Reviews Tasks Ready (JavaScript)

Source: https://docs.dataforseo.com/v3/merchant/google/reviews/tasks_ready

This JavaScript (Node.js) example uses the `axios` library to make a GET request to the DataForSEO API for merchant Google reviews tasks. It demonstrates using `auth` for credentials and handling the response or errors.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/merchant/google/reviews/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch Live Domain Technologies using Bash

Source: https://docs.dataforseo.com/v3/domain_analytics/technologies/domain_technologies/live

This snippet demonstrates how to fetch live domain technologies using a Bash script with cURL. It involves encoding credentials and sending a POST request to the Dataforseo API. Ensure you replace 'login' and 'password' with your actual API credentials.

```bash
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access 

login="login" 

password="password" 

cred="$(printf ${login}:${password} | base64)" 

curl --location --request POST "https://api.dataforseo.com/v3/domain_analytics/technologies/domain_technologies/live" 

--header "Authorization: Basic ${cred}"  

--header "Content-Type: application/json" 

--data-raw "[

    {

        "target": "dataforseo.com"

    }

]"
```

--------------------------------

### JavaScript (Node.js): Perform Google Domain Intersection Analysis

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live

This Node.js example uses the 'axios' library to send a POST request to the DataForSEO API for domain intersection analysis. It demonstrates how to configure the request with authentication, request body, and headers. Ensure you have 'axios' installed (`npm install axios`).

```javascript
const post_array = [];



post_array.push({

  "target1": "cnn.com",

  "target2": "forbes.com",

  "language_name": "English",

  "location_code": 2840,

  "filters": [

    ["first_domain_serp_element.etv", ">", 0]

  ],

  "limit": 3

});



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Fetch Bing Keywords for Site using PHP

Source: https://docs.dataforseo.com/v3/keywords_data/bing/keywords_for_site/tasks_ready

This PHP example demonstrates how to use the RestClient library to fetch Bing keywords for a site from the Dataforseo API. It handles API initialization, making the GET request, and error handling.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {

    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

    $client = new RestClient($api_url, null, 'login', 'password');

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

    exit();

}

try {

    // using this method you can get a list of completed tasks

    // GET /v3/keywords_data/bing/keywords_for_site/tasks_ready

    // in addition to 'keywords_for_site' you can also set other parameters

    // the full list of possible parameters is available in documentation

    $result = $client->get('/v3/keywords_data/bing/keywords_for_site/tasks_ready');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### Initialize DataForSEO Client and Get Tasks using Python

Source: https://docs.dataforseo.com/v3/serp/baidu/organic/task_get/html

This Python script demonstrates how to initialize the RestClient for the DataForSEO API with provided login credentials. It then makes a GET request to retrieve a list of ready tasks for Baidu organic search. The response from this request is stored and can be further processed to fetch individual task results.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# 1 - using this method you can get a list of completed tasks
# GET /v3/serp/baidu/organic/tasks_ready
# in addition to 'baidu' and 'organic' you can also set other search engine and type parameters
# the full list of possible parameters is available in documentation
response = client.get("/v3/serp/baidu/organic/tasks_ready")

```

--------------------------------

### Fetch Google Questions and Answers Tasks Ready (Bash)

Source: https://docs.dataforseo.com/v3/business_data/google/questions_and_answers/tasks_ready

This Bash script demonstrates how to authenticate with the DataForSEO API using basic authentication and fetch a list of ready tasks for Google Questions and Answers. It constructs a base64 encoded credential string and sends a GET request to the tasks_ready endpoint.

```bash
login="login"

password="password"

cred="$(printf ${login}:${password} | base64)"

curl --location --request GET "https://api.dataforseo.com/v3/business_data/google/questions_and_answers/tasks_ready" \

--header "Authorization: Basic ${cred}"  \

--header "Content-Type: application/json" \

--data-raw ""
```

--------------------------------

### GET /v2/cmn_user

Source: https://docs.dataforseo.com/v2/cmn_java=

Retrieves information about the current user. The response includes a 'results' array containing user details.

```APIDOC
## GET /v2/cmn_user

### Description
Retrieves information about the current user. The response contains a JSON array in the `results` field with user details.

### Method
GET

### Endpoint
/v2/cmn_user

### Parameters
#### Query Parameters
None

#### Request Body
None

### Request Example
```
curl "https://api.dataforseo.com/v2/cmn_user"
```

### Response
#### Success Response (200)
- **status** (string) - General result ('ok' or 'error').
- **error** (array) - Informational array of errors (only if status='error'). Contains 'code' (integer) and 'message' (string).
- **results** (array) - Array containing user information.

#### Response Example
```json
{
    "status": "ok",
    "results": [
        {
            "user_id": 12345,
            "email": "user@example.com",
            "status": "active",
            "created_at": "2023-01-01 10:00:00",
            "updated_at": "2023-01-01 10:00:00"
        }
    ]
}
```

#### Error Response Example
```json
{
    "status": "error",
    "error": [
        {
            "code": 101,
            "message": "Authorization was not provided."
        }
    ]
}
```
```

--------------------------------

### Get Google SERP Autocomplete Tasks Ready in Python

Source: https://docs.dataforseo.com/v3/serp/google/autocomplete/task_get/advanced_bash=

This Python snippet uses the `RestClient` class to fetch a list of completed Google SERP autocomplete tasks. It requires your API login and password for authentication. The example demonstrates how to initialize the client and make a GET request to the `tasks_ready` endpoint. Ensure you have the `python_Client.zip` library.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# 1 - using this method you can get a list of completed tasks
# GET /v3/serp/google/autocomplete/tasks_ready
# the full list of possible parameters is available in documentation
response = client.get("/v3/serp/google/autocomplete/tasks_ready")

```

--------------------------------

### GET /v2/cmn_se

Source: https://docs.dataforseo.com/v2/cmn_java=

Retrieves common search engine data. This endpoint requires Basic Authentication with your DataForSEO credentials.

```APIDOC
## GET /v2/cmn_se

### Description
This endpoint retrieves common search engine data. It's useful for gathering general search engine information.

### Method
GET

### Endpoint
https://api.dataforseo.com/v2/cmn_se

### Parameters

#### Query Parameters
None

#### Headers
- **Authorization** (string) - Required - Basic authentication token (e.g., "Basic base64EncodedCredentials")

### Request Example
```bash
curl -X GET "https://api.dataforseo.com/v2/cmn_se"
     -H "Authorization: Basic YOUR_BASE64_ENCODED_CREDENTIALS"
```

### Response
#### Success Response (200)
- **status** (string) - The status of the API request. Should be 'ok' for success.
- **results** (array) - An array containing the search engine data.

#### Error Response (e.g., 401, 400)
- **status** (string) - The status of the API request. Should be 'error' for failures.
- **error** (object) - An object containing error details.
    - **code** (integer) - The error code.
    - **message** (string) - A description of the error.

### Response Example (Success)
```json
{
    "status": "ok",
    "results": [
        {
            "some_metric": "some_value"
        }
    ]
}
```

### Response Example (Error)
```json
{
    "status": "error",
    "error": {
        "code": 401,
        "message": "Unauthorized"
    }
}
```
```

--------------------------------

### Get Ready Google Review Tasks using Bash

Source: https://docs.dataforseo.com/v3/reviews-tasks_ready

This Bash script demonstrates how to authenticate with the Dataforseo API using a base64 encoded username and password, and then makes a GET request to retrieve ready Google review tasks. It sets the Authorization and Content-Type headers. Ensure you replace 'login' and 'password' with your actual API credentials.

```bash
login="login"
password="password"
cred="$(printf ${login}:${password} | base64)"

curl --location --request GET "https://api.dataforseo.com/v3/reviews/google/tasks_ready" \
--header "Authorization: Basic ${cred}" \
--header "Content-Type: application/json"
```

--------------------------------

### Authenticate and Fetch Locations via Node.js (axios)

Source: https://docs.dataforseo.com/v3/ai_optimization/chat_gpt/llm_scraper/locations

This Node.js example uses the 'axios' library to make a GET request to the Dataforseo API. It demonstrates how to set up authentication using basic auth with your login and password, and specifies the content type. The response data, specifically the 'result' from the first task, is logged to the console.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/ai_optimization/chat_gpt/llm_scraper/locations',

    auth: {

        username: 'login',

        password: 'password'

    },

    data: [{

        country: "us"

    }],

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get Keyword ID (C#)

Source: https://docs.dataforseo.com/v2/cmn_csharp=

This endpoint retrieves a unique identifier for a given keyword. Use your API credentials from the DataForSEO dashboard for authentication.

```APIDOC
## GET /v2/cmn_key_id/{keyword}

### Description
Retrieves a unique identifier (key ID) for a specified keyword. This ID can be used for subsequent API calls that require a keyword identifier.

### Method
GET

### Endpoint
`/v2/cmn_key_id/{keyword}`

### Parameters
#### Path Parameters
- **keyword** (string) - Required - The keyword for which to retrieve the ID. URL-encoded.

### Request Example
```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task CmnKeyIdAsync()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                // Replace 'login' and 'password' with your actual credentials
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };

            string keyword = "online rank checker";
            string encodedKeyword = Uri.EscapeDataString(keyword);
            string endpoint = $"v2/cmn_key_id/{encodedKeyword}";

            try
            {
                HttpResponseMessage response = await httpClient.GetAsync(endpoint);
                string responseBody = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    // Process successful response
                    Console.WriteLine($"Success: {responseBody}");
                    // Example of parsing JSON response:
                    // var result = JsonConvert.DeserializeObject<YourResponseType>(responseBody);
                    // Console.WriteLine($"Key ID: {result.results[0].key_id}");
                }
                else
                {
                    // Process error response
                    Console.WriteLine($"Error: {response.StatusCode} - {responseBody}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Exception: {ex.Message}");
            }
            finally
            {
                httpClient.Dispose();
            }
        }
    }
}
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the response ('success' or 'error').
- **results** (array) - An array containing the keyword ID if successful.
  - **key_id** (string) - The unique identifier for the keyword.

#### Response Example
```json
{
    "status": "success",
    "results": [
        {
            "key_id": "some_unique_keyword_id"
        }
    ]
}
```

#### Error Response (e.g., 401, 404)
- **status** (string) - Indicates the status of the response ('error').
- **error** (object) - Contains error details.
  - **code** (integer) - The error code.
  - **message** (string) - A human-readable error message.
  - **url** (string) - The URL that caused the error.

#### Error Response Example
```json
{
    "status": "error",
    "error": {
        "code": 401,
        "message": "Invalid credentials provided.",
        "url": "/v2/cmn_key_id/online%20rank%20checker"
    }
}
```
```

--------------------------------

### Perform Live Lighthouse Audit with PHP

Source: https://docs.dataforseo.com/v3/on_page/lighthouse/live/json

This PHP example shows how to perform a live Lighthouse audit using the RestClient. It includes setting up API credentials and constructing an array of tasks, each with a URL and optional parameters. The code handles potential RestClient exceptions and prints the API response.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');



$post_array = array();

// example #1 - a simple way to set a task

$post_array[] = array(
   "url" => "https://dataforseo.com",
   "for_mobile" => true
);

// example #2 - a way to set a task with additional parameters

$post_array[] = array(
   "url" => "https://dataforseo.com",
   "for_mobile" => true,
   "tag" => "some_string_123"
);



// this example has a 2 elements, but in the case of large number of tasks - send up to 100 elements per POST request

if (count($post_array) > 0) {

   try {

      // POST /v3/on_page/lighthouse/live/json

      // the full list of possible parameters is available in documentation

      $result = $client->post('/v3/on_page/lighthouse/live/json', $post_array);

      print_r($result);

      // do something with post result

   } catch (RestClientException $e) {

      echo "n";

      print "HTTP code: {$e->getHttpCode()}n";

      print "Error code: {$e->getCode()}n";

      print "Message: {$e->getMessage()}n";

      print  $e->getTraceAsString();

      echo "n";

   }

}

$client = null;

?>
```

--------------------------------

### Make Google Keyword Suggestions API Call in C#

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live

This C# example demonstrates how to use the DataForSEO Labs Google Keyword Suggestions API. It sets up an HttpClient with authentication, prepares POST data including keyword and location parameters, sends the request, and then deserializes the JSON response. It also includes logic to check the status code and print results or errors.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_google_keyword_suggestions_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))

                }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                keyword = "phone",

                location_name = "United States",

                language_name = "English",

                include_serp_info = true,

                include_seed_keyword = true,

                limit = 1

            });

            // POST /v3/dataforseo_labs/google/keyword_suggestions/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/google/keyword_suggestions/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Keyword ID (Python)

Source: https://docs.dataforseo.com/v2/cmn_csharp=

This endpoint retrieves a unique identifier for a given keyword. Use your API credentials from the DataForSEO dashboard for authentication.

```APIDOC
## GET /v2/cmn_key_id/{keyword}

### Description
Retrieves a unique identifier (key ID) for a specified keyword. This ID can be used for subsequent API calls that require a keyword identifier.

### Method
GET

### Endpoint
`/v2/cmn_key_id/{keyword}`

### Parameters
#### Path Parameters
- **keyword** (string) - Required - The keyword for which to retrieve the ID. URL-encoded.

### Request Example
```python
from client import RestClient

# Replace 'login' and 'password' with your actual credentials
client = RestClient("login", "password")
keyword = "online rank checker"
response = client.get(f"/v2/cmn_key_id/{keyword}")

if response["status"] == "error":
    print(f"error. Code: {response['error']['code']} Message: {response['error']['message']}")
else:
    print(response["results"][0]["key_id"])
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the response ('success' or 'error').
- **results** (array) - An array containing the keyword ID if successful.
  - **key_id** (string) - The unique identifier for the keyword.

#### Response Example
```json
{
    "status": "success",
    "results": [
        {
            "key_id": "some_unique_keyword_id"
        }
    ]
}
```

#### Error Response (e.g., 401, 404)
- **status** (string) - Indicates the status of the response ('error').
- **error** (object) - Contains error details.
  - **code** (integer) - The error code.
  - **message** (string) - A human-readable error message.
  - **url** (string) - The URL that caused the error.

#### Error Response Example
```json
{
    "status": "error",
    "error": {
        "code": 401,
        "message": "Invalid credentials provided.",
        "url": "/v2/cmn_key_id/online%20rank%20checker"
    }
}
```
```

--------------------------------

### C#: Get Common Locations for Keyword Finder

Source: https://docs.dataforseo.com/v2/cmn_java=

This C# code example demonstrates how to make an API request to retrieve common locations for keyword finder statistics. It uses HttpClient for making the request and basic authentication with API credentials. The response is handled asynchronously.

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task cmn_locations_stat_kwrd_finder()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))
            }
            };
            var response = await httpClient.GetAsync("v2/cmn_locations_stat_kwrd_finder");
        }
    }
}

```

--------------------------------

### Fetch Ready Tasks using Bash

Source: https://docs.dataforseo.com/v3/keywords_data/google/keywords_for_keywords/tasks_ready

This Bash script demonstrates how to authenticate with the DataForSEO API using basic authentication and fetch a list of ready tasks. It encodes login credentials and sends a GET request to the tasks_ready endpoint.

```bash
login="login"

password="password"

cred="$(printf ${login}:${password} | base64)"

curl --location --request GET "https://api.dataforseo.com/v3/keywords_data/google/keywords_for_keywords/tasks_ready" \

--header "Authorization: Basic ${cred}"  \

--header "Content-Type: application/json" \

--data-raw ""
```

--------------------------------

### Get Keyword ID (PHP)

Source: https://docs.dataforseo.com/v2/cmn_csharp=

This endpoint retrieves a unique identifier for a given keyword. Use your API credentials from the DataForSEO dashboard for authentication.

```APIDOC
## GET /v2/cmn_key_id/{keyword}

### Description
Retrieves a unique identifier (key ID) for a specified keyword. This ID can be used for subsequent API calls that require a keyword identifier.

### Method
GET

### Endpoint
`/v2/cmn_key_id/{keyword}`

### Parameters
#### Path Parameters
- **keyword** (string) - Required - The keyword for which to retrieve the ID. URL-encoded.

### Request Example
```php
<?php
require('RestClient.php');

try {
    // Replace 'login' and 'password' with your actual credentials
    $client = new RestClient('https://api.dataforseo.com/', null, 'login', 'password');
    $keyword = urlencode('online rank checker');
    $key_get_result = $client->get("v2/cmn_key_id/{$keyword}");
    print_r($key_get_result);
} catch (RestClientException $e) {
    echo "HTTP code: ". $e->getHttpCode() . "\n";
    echo "Error code: ". $e->getCode() . "\n";
    echo "Message: ". $e->getMessage() . "\n";
    echo $e->getTraceAsString();
    exit();
}
$client = null;
?>
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the response ('success' or 'error').
- **results** (array) - An array containing the keyword ID if successful.
  - **key_id** (string) - The unique identifier for the keyword.

#### Response Example
```json
{
    "status": "success",
    "results": [
        {
            "key_id": "some_unique_keyword_id"
        }
    ]
}
```

#### Error Response (e.g., 401, 404)
- **status** (string) - Indicates the status of the response ('error').
- **error** (object) - Contains error details.
  - **code** (integer) - The error code.
  - **message** (string) - A human-readable error message.
  - **url** (string) - The URL that caused the error.

#### Error Response Example
```json
{
    "status": "error",
    "error": {
        "code": 401,
        "message": "Invalid credentials provided.",
        "url": "/v2/cmn_key_id/online%20rank%20checker"
    }
}
```
```

--------------------------------

### Fetch Google Jobs SERP Tasks Ready via API

Source: https://docs.dataforseo.com/v3/serp/google/jobs/tasks_ready_php=

This C# example demonstrates how to make an authenticated GET request to the DataForSEO API to check for completed Google Jobs SERP tasks. It sets up an HttpClient with basic authentication and deserializes the JSON response. The example also shows how to handle successful responses (status code 20000) and errors.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/serp/google/jobs/tasks_ready

            // in addition to 'google' and 'jobs' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/serp/google/jobs/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Fetch Google Local Finder Tasks Ready via Bash

Source: https://docs.dataforseo.com/v3/serp/google/local_finder/tasks_ready

This Bash script demonstrates how to authenticate with the DataForSEO API using basic authentication and retrieve a list of ready tasks for Google Local Finder. It requires user credentials and uses `curl` for making the GET request. The output is the raw JSON response from the API.

```bash
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access 

login="login" 

password="password" 

cred="$(printf ${login}:${password} | base64)" 

curl --location --request GET "https://api.dataforseo.com/v3/serp/google/local_finder/tasks_ready" 

--header "Authorization: Basic ${cred}"  

--header "Content-Type: application/json" 

--data-raw ""
```

--------------------------------

### Fetch Bing Local Pack Tasks (PHP)

Source: https://docs.dataforseo.com/v3/serp/bing/local_pack/tasks_fixed

This PHP example utilizes the provided `RestClient.php` class to interact with the DataForSEO API. It shows how to initialize the client with credentials, make a GET request to retrieve Bing local pack tasks, and handle potential `RestClientException` errors. The result is printed using `print_r`.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {

    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

    $client = new RestClient($api_url, null, 'login', 'password');

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

    exit();

}

try {

    // using this method you can get a list of completed tasks

    // GET /v3/serp/bing/local_pack/tasks_fixed

    // in addition to 'bing' and 'local_pack' you can also set other search engine and type parameters

    // the full list of possible parameters is available in documentation

    $result = $client->get('/v3/serp/bing/local_pack/tasks_fixed');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### Fetch DataForSEO Apple App Searches by ID in C#

Source: https://docs.dataforseo.com/v3/app_data/apple/app_searches/task_get/advanced

This C# example demonstrates how to use the DataForSEO API to get the results of an app search task by its ID. It includes setting up the HTTP client, making the GET request, and deserializing the JSON response. Error handling for the API call and task status is also included.

```csharp
using Newtonsoft.Json;
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task app_data_apple_app_searches_task_get_by_id()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };

            // get the task results by id
            // GET /v3/app_data/apple/app_searches/task_get/advanced/$id
            // use the task identifier that you recieved upon setting a task
            string id = "06141103-2692-0309-1000-980b778b6d25";
            var taskGetResponse = await httpClient.GetAsync("/v3/app_data/apple/app_searches/task_get/advanced/" + id);
            var result = JsonConvert.DeserializeObject<dynamic>(await taskGetResponse.Content.ReadAsStringAsync());

            if (result.tasks != null)
            {
                var fst = result.tasks.First;
                // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
                if (fst.status_code >= 40000 || fst.result == null)
                    Console.WriteLine($"error. Code: {fst.status_code} Message: {fst.status_message}");
                else
                    // do something with result
                    Console.WriteLine(String.Join(Environment.NewLine, fst));
            }
            else
                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");
        }
    }
}
```

--------------------------------

### Fetch Keyword Finder Suggest Tasks (C#)

Source: https://docs.dataforseo.com/v2/kwrd_finder_python=

This C# code snippet demonstrates how to fetch keyword finder suggest tasks using the DataForSEO API. It sets up an HttpClient with basic authentication, makes a GET request to the API, and deserializes the JSON response. The code handles errors and iterates through completed tasks, printing them to the console. Dependencies include System.Net.Http, System.Text, and Newtonsoft.Json.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task kwrd_finder_suggest_tasks_get()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),

                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))}
            };
            var completedTasksResponse = await httpClient.GetAsync("v2/kwrd_finder_suggest_tasks_get");
            var completedTasksObj = JsonConvert.DeserializeObject(await completedTasksResponse.Content.ReadAsStringAsync());
            if (completedTasksObj.status == "error")
                Console.WriteLine($"error. Code: {completedTasksObj.error.code} Message: {completedTasksObj.error.message}");
            else if (completedTasksObj.results_count != 0)
            {
                foreach (var result in completedTasksObj.results)
                {
                    var completedTask = ((IEnumerable)result).First();
                    Console.WriteLine(completedTask);
                }
            }
            else
                Console.WriteLine("No completed tasks");
        }
    }
}
```

--------------------------------

### Get Clickstream Locations and Languages (Node.js)

Source: https://docs.dataforseo.com/v3/keywords_data/clickstream_data/locations_and_languages

This Node.js example uses the 'request' module to make a GET request to the DataForSEO Clickstream Data API for locations and languages. It includes an 'Authorization' header with a pre-encoded credential. The response body is logged to the console.

```javascript
var request = require('request');

var options = {

  'method': 'GET',

  'url': 'https://api.dataforseo.com/v3/keywords_data/clickstream_data/locations_and_languages',

  'headers': {

    'Authorization': 'Basic c3VwcG9ydEBkYXRhZm9yc2VvLmNvbTpTUnJYVHp2UGtFSjgzdXlz'

  }

};

request(options, function (error, response) {

  if (error) throw new Error(error);

  console.log(response.body);

});
```

--------------------------------

### C#: Generate Content Live with DataForSeo API

Source: https://docs.dataforseo.com/v3/content_generation/generate/live

This C# example demonstrates how to call the DataForSeo content generation API. It sets up an HttpClient with authentication, prepares the POST data including text generation parameters, sends the request, and deserializes the JSON response. It also includes error handling based on the status code.

```csharp
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task content_generation_generate_live()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };

            var postData = new List<object>();
            postData.Add(new
            {
                text = "SEO is",
                max_new_tokens = 100,
                repetition_penalty = 1.01,
                stop_words = new[]
                {
                    "123",
                    "n"
                },
                creativity_index = 1,
                avoid_starting_words = new[]
                {
                    "SEO",
                    "search engine optimization",
                    "SEO is",
                }
            });

            // POST /v3/content_generation/generate/live
            // the full list of possible parameters is available in documentation
            var taskPostResponse = await httpClient.PostAsync("/v3/content_generation/generate/live", new StringContent(JsonConvert.SerializeObject(postData)));
            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
            if (result.status_code == 20000)
            {
                // do something with result
                Console.WriteLine(result);
            }
            else
                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");
        }
    }
}

```

--------------------------------

### Get Bing Ads Audience Estimation Industries List (PHP)

Source: https://docs.dataforseo.com/v3/keywords_data/bing/audience_estimation/industries

Retrieves the list of industries for Bing Ads Audience Estimation using a PHP REST client. This example demonstrates making a GET request and handling potential errors.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');



try {

    // using this method you can get a list of industries

    // GET /v3/keywords_data/bing/audience_estimation/industries

    $result = $client->get('/v3/keywords_data/bing/audience_estimation/industries');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### Fetch Phrase Trends Live using Node.js

Source: https://docs.dataforseo.com/v3/content_analysis/phrase_trends/live

This JavaScript example uses the popular 'axios' library to send a POST request to the DataForSEO API for phrase trends. It demonstrates setting up the request with the API endpoint, authentication using basic auth, constructing the JSON data payload, and handling the response or errors. Ensure you have 'axios' installed (`npm install axios`).

```javascript
const post_array = [];

post_array.push({
        "keyword": "logitech",
        "search_mode": "as_is",
        "date_from": "2022-09-01",
        "date_group": "month"
});

const axios = require('axios');

axios({
  method: 'post',
  url: 'https://api.dataforseo.com/v3/content_analysis/phrase_trends/live',
  auth: {
    username: 'login',
    password: 'password'
  },
  data: post_array,
  headers: {
    'content-type': 'application/json'
  }
}).then(function (response) {
  var result = response['data']['tasks'];
  // Result data
  console.log(result);
}).catch(function (error) {
  console.log(error);
});
```

--------------------------------

### Retrieve Google Product Task Results (C#)

Source: https://docs.dataforseo.com/v3/merchant/google/products/task_get/html_php=

This C# example demonstrates how to fetch Google product task results using HttpClient. It first retrieves a list of ready tasks, then iterates through them to get individual task results via HTML endpoints or task IDs. Error handling and JSON deserialization are included.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task merchant_google_products_task_get()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // #1 - using this method you can get a list of completed tasks

            // GET /v3/merchant/google/products/tasks_ready

            var response = await httpClient.GetAsync("/v3/merchant/google/products/tasks_ready");

            var tasksInfo = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            var tasksResponses = new List<object>();

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (tasksInfo.status_code == 20000)

            {

                if (tasksInfo.tasks != null)

                {

                    foreach (var tasks in tasksInfo.tasks)

                    {

                        if (tasks.result != null)

                        {

                            foreach (var task in tasks.result)

                            {

                                if (task.endpoint_html != null)

                                {

                                    // #2 - using this method you can get results of each completed task

                                    // GET /v3/merchant/google/products/task_get/html/$id

                                    var taskGetResponse = await httpClient.GetAsync((string)task.endpoint_html);

                                    var taskResultObj = JsonConvert.DeserializeObject<dynamic>(await taskGetResponse.Content.ReadAsStringAsync());

                                    if (taskResultObj.tasks != null)

                                    {

                                        var fst = taskResultObj.tasks.First;

                                        // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

                                        if (fst.status_code >= 40000 || fst.result == null)

                                            Console.WriteLine($"error. Code: {fst.status_code} Message: {fst.status_message}");

                                        else

                                            tasksResponses.Add(fst.result);

                                    }

                                    // #3 - another way to get the task results by id

                                    // GET /v3/merchant/google/products/task_get/html/$id

                                    /*

                                    var tasksGetResponse = await httpClient.GetAsync("/v3/merchant/google/products/task_get/html/" + (string)task.id);

                                    var taskResultObj = JsonConvert.DeserializeObject<dynamic>(await tasksGetResponse.Content.ReadAsStringAsync());

                                    if (taskResultObj.tasks != null)

                                    {

                                        var fst = taskResultObj.tasks.First;

                                        // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors


```

--------------------------------

### Retrieve Business Data Tasks Ready Status in C#

Source: https://docs.dataforseo.com/v3/business_data/google/hotel_info/tasks_ready

This C# example shows how to call the DataForSEO API to get a list of completed tasks for Google Hotel Info. It uses HttpClient to make a GET request, includes basic authentication, and deserializes the JSON response using Newtonsoft.Json. The code checks the 'status_code' in the response to determine if the operation was successful.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task business_data_info_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/business_data/google/hotel_info/tasks_ready

            var response = await httpClient.GetAsync("/v3/business_data/google/hotel_info/tasks_ready");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}
```

--------------------------------

### Fetch Google Locations Data using DataForSEO API (C#)

Source: https://docs.dataforseo.com/v3/keywords_data/google/locations

This C# example shows how to make an authenticated GET request to the DataForSEO API to retrieve Google locations. It utilizes HttpClient and Newtonsoft.Json for deserialization. The code includes error handling based on the 'status_code' in the response, similar to the Python example.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_locations()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of locations

            // GET /v3/keywords_data/google/locations

            // in addition to 'google' you can also set other search engine

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/keywords_data/google/locations");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}
```

--------------------------------

### Example API Request and Response

Source: https://docs.dataforseo.com/v3/merchant/google/sellers/task_post

Illustrative examples demonstrating how to make a request to the Google Shopping API and the expected JSON response structure. This includes sample values for parameters like `language_code`, `se_domain`, and the format of the returned task information.

```N/A
Example `language_code`: `en`
Example `se_domain`: `google.co.uk`
Example `additional_specifications`: {
 "eto": "16157121050167572763_0"
}
Example `postback_url`: `http://your-server.com/postbackscript?id=$id&tag=$tag`
```

--------------------------------

### Fetch Google Finance Explore Tasks Ready using Python

Source: https://docs.dataforseo.com/v3/serp/google/finance_explore/tasks_ready

This Python example shows how to use a custom RestClient to interact with the Dataforseo API. It specifically calls the 'serp/google/finance_explore/tasks_ready' endpoint using the client's get method. Ensure you have the client.py file and replace placeholder credentials.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# using this method you can get a list of completed tasks
# GET /v3/serp/google/finance_explore/tasks_ready
# in addition to 'google' and 'finance_explore' you can also set other search engine and type parameters
# the full list of possible parameters is available in documentation
response = client.get("/v3/serp/google/finance_explore/tasks_ready")
```

--------------------------------

### Fetch Google Maps Task Results with Node.js (Axios)

Source: https://docs.dataforseo.com/v3/serp/google/maps/task_get/advanced

This Node.js snippet uses the Axios library to make a GET request to the DataForSEO API to fetch advanced Google Maps task results. It includes basic authentication and error handling. Ensure Axios is installed (`npm install axios`).

```javascript
const task_id = '02231256-2604-0066-2000-57133b8fc54e';



const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/google/maps/task_get/advanced/' + task_id,

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### C# Example: Get Similar Keywords via DataForSeo API

Source: https://docs.dataforseo.com/v2/kwrd_finder_python=

This C# code snippet demonstrates how to retrieve similar keywords using the DataForSeo API. It sets up an HttpClient with basic authentication, constructs a POST request with specified keyword, country, language, and filter parameters, and then deserializes and processes the JSON response. Dependencies include Newtonsoft.Json and System.Net.Http.

```csharp
public static async Task kwrd_finder_similar_keywords_get()
{
    var httpClient = new HttpClient
    {
        BaseAddress = new Uri("https://api.dataforseo.com/"),
        //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
        DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
    };

    var rnd = new Random(); //you can set as "index of post_data" your ID, string, etc. we will return it with all results.
    var postObject = new Dictionary<int, object>
    {
        [rnd.Next(1, 30000000)] = new
        {
            keyword = "ice tea",
            country_code = "US",
            language = "en",
            limit = 10,
            offset = 0,
            orderby = "cpc,desc",
            filters = new object[]
            {
                new object[] { "cpc", ">", 0 },
                "or",
                new object[]
                {
                    new object[] { "search_volume", ">", 0 },
                    "and",
                    new object[] { "search_volume", "<= ", 1000 }
                }
            }
        }
    };
    var pagePostResponse = await httpClient.PostAsync("v2/kwrd_finder_similar_keywords_get", new StringContent(JsonConvert.SerializeObject(new { data = postObject })))
    var obj = JsonConvert.DeserializeObject(await pagePostResponse.Content.ReadAsStringAsync());
    foreach (var result in obj.results)
    {
        var taskState = ((IEnumerable)result).First();
        if (taskState.status == "error")
            Console.WriteLine($"Error in task with post_id {taskState.post_id}. Code: {taskState.error.code} Message: {taskState.error.message}");
        Console.WriteLine(taskState);
    }
}
```

--------------------------------

### Fetch Google Search Volume Tasks Ready via DataForSEO API

Source: https://docs.dataforseo.com/v3/keywords_data/google/search_volume/tasks_ready

This C# example demonstrates how to use the HttpClient to make a GET request to the '/v3/keywords_data/google/search_volume/tasks_ready' endpoint. It includes setting up authentication with basic credentials and deserializing the JSON response. The code handles both successful responses and errors based on the status code.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/keywords_data/google/search_volume/tasks_ready

            // in addition to 'search_volume' you can also set other parameters

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/keywords_data/google/search_volume/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Fetch YouTube Video Info using Node.js (axios)

Source: https://docs.dataforseo.com/v3/serp/youtube/video_info/task_get/advanced

This JavaScript example uses the 'axios' library to make a GET request to the DataForSEO API for YouTube video information. It demonstrates how to set up authentication, specify the endpoint, and handle the response or errors.

```javascript
const task_id = '02231256-2604-0066-2000-57133b8fc54e';



const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/youtube/video_info/task_get/advanced/' + task_id,

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});

```

--------------------------------

### Perform On-Page Keyword Density Analysis (C#)

Source: https://docs.dataforseo.com/v3/on_page/keyword_density

This C# code example shows how to perform an on-page keyword density analysis using the DataForSeo API. It includes setting up an HttpClient with authentication, constructing a POST request with specific parameters like 'id', 'page_from', 'keyword_length', and 'filters', and deserializing the JSON response. It also includes error handling based on the status code.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task on_page_keyword_density()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            // simple way to get a result

            postData.Add(new

            {

                id = "07281559-0695-0216-0000-c269be8b7592",

                page_from = "/apis/google-trends-api",

                keyword_length: 2,

                filters = new object[]

                {

                    new object[] { "frequency", ">", 5 }

                }

            });

            // POST /v3/on_page/keyword_density

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/on_page/keyword_density", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}
```

--------------------------------

### Get Google Review Tasks Ready (Bash)

Source: https://docs.dataforseo.com/v3/business_data/google/reviews/tasks_ready

This Bash script demonstrates how to fetch a list of ready Google review tasks from the DataForSEO API. It constructs a base64 encoded authorization token using provided login and password credentials and then makes a GET request to the 'tasks_ready' endpoint.

```bash
#!/bin/bash

# Replace with your actual credentials from https://app.dataforseo.com/api-access
login="login"
password="password"

# Encode credentials for Basic Authentication
cred="$(printf ${login}:${password} | base64)"

# Make the API request to get ready tasks
curl --location --request GET "https://api.dataforseo.com/v3/business_data/google/reviews/tasks_ready" \
--header "Authorization: Basic ${cred}" \
--header "Content-Type: application/json"
```

--------------------------------

### GET /v2/cmn_locations_stat_kwrd_finder

Source: https://docs.dataforseo.com/v2/cmn_csharp=

Retrieves statistics for common locations related to keyword finding. This endpoint requires authentication and returns a list of locations with their associated counts.

```APIDOC
## GET /v2/cmn_locations_stat_kwrd_finder

### Description
This endpoint retrieves statistics for common locations relevant to keyword research. It returns a list of locations, each with a canonical name, country code, language, and a count representing its relevance or volume.

### Method
GET

### Endpoint
https://api.dataforseo.com/v2/cmn_locations_stat_kwrd_finder

### Parameters

#### Query Parameters
(No query parameters are explicitly defined in the provided code, but typically API endpoints may have parameters for filtering or pagination.)

#### Request Body
This endpoint does not typically use a request body for GET requests.

### Request Example
```bash
curl -X GET https://api.dataforseo.com/v2/cmn_locations_stat_kwrd_finder \
     -H "Authorization: Basic <base64_encoded_credentials>"
```

### Response
#### Success Response (200)
- **status** (string) - The status of the API request ('ok' or 'error').
- **results_time** (string) - The time taken to process the request.
- **results_count** (integer) - The total number of results returned.
- **results** (array) - An array of location statistics objects.
  - **loc_id** (integer) - The unique identifier for the location.
  - **loc_name_canonical** (string) - The canonical name of the location.
  - **country_code** (string) - The two-letter country code.
  - **language** (string) - The language code.
  - **count** (integer) - The associated count for the location.

#### Response Example
```json
{
    "status": "ok",
    "results_time": "5.7730 sec.",
    "results_count": 6,
    "results": [
        {
            "loc_id": 2840,
            "loc_name_canonical": "United States",
            "country_code": "US",
            "language": "en",
            "count": 158397916
        },
        {
            "loc_id": 2826,
            "loc_name_canonical": "United Kingdom",
            "country_code": "GB",
            "language": "en",
            "count": 31516738
        }
    ]
}
```

#### Error Response (e.g., 4xx or 5xx)
- **status** (string) - 'error'.
- **error** (object) - Contains error details.
  - **code** (integer) - The error code.
  - **message** (string) - A description of the error.

#### Error Response Example
```json
{
    "status": "error",
    "error": {
        "code": 401,
        "message": "Invalid credentials"
    }
}
```
```

--------------------------------

### Fetch Google My Business Tasks Ready (Python)

Source: https://docs.dataforseo.com/v3/business_data/google/my_business_info/tasks_ready

A Python example demonstrating how to fetch completed Google My Business tasks using a custom RestClient. It requires the client.py file and API credentials.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip

client = RestClient("login", "password")
# using this method you can get a list of completed tasks
# GET /v3/business_data/google/my_business_info/tasks_ready
response = client.get("/v3/business_data/google/my_business_info/tasks_ready")
```

--------------------------------

### Fetch Ready Tasks using Python

Source: https://docs.dataforseo.com/v3/serp/google/jobs/tasks_ready

This Python example utilizes the provided RestClient class to retrieve a list of completed tasks from the 'tasks_ready' API endpoint. It initializes the client with login credentials and makes a GET request. The response is stored in the 'response' variable.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# using this method you can get a list of completed tasks
# GET /v3/serp/google/jobs/tasks_ready
# in addition to 'google' and 'jobs' you can also set other search engine and type parameters
# the full list of possible parameters is available in documentation
response = client.get("/v3/serp/google/jobs/tasks_ready")
```

--------------------------------

### GET /v2/cmn_locations_stat_kwrd_finder

Source: https://docs.dataforseo.com/v2/cmn_csharp=

This endpoint retrieves data related to keyword finder for common locations. It requires basic authentication and returns results or error information.

```APIDOC
## GET /v2/cmn_locations_stat_kwrd_finder

### Description
Retrieves keyword popularity and related data for specified locations. This is useful for understanding search trends and keyword relevance in different geographical areas.

### Method
GET

### Endpoint
https://api.dataforseo.com/v2/cmn_locations_stat_kwrd_finder

### Parameters
#### Query Parameters
- **api_key** (string) - Required - Your DataForSeo API key for authentication.
- **keyword** (string) - Optional - The keyword for which to find location statistics.
- **location_code** (integer) - Optional - The code of the location for which to retrieve data.

### Request Example
```bash
curl -X GET "https://api.dataforseo.com/v2/cmn_locations_stat_kwrd_finder?keyword=example_keyword&location_code=123" \
     -H "Authorization: Basic YOUR_BASE64_ENCODED_CREDENTIALS"
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the operation ('ok' or 'error').
- **results** (array) - An array of objects, where each object contains location statistics for the keyword.
- **error** (object) - Contains error details if the status is 'error'.
  - **code** (integer) - The error code.
  - **message** (string) - The error message.

#### Response Example
```json
{
    "status": "ok",
    "results": [
        {
            "keyword": "example_keyword",
            "location_code": 123,
            "search_volume": 1000,
            "competition_level": "high"
        }
    ]
}
```

#### Error Response Example (401)
```json
{
    "status": "error",
    "error": {
        "code": 401,
        "message": "Unauthorized."
    }
}
```
```

--------------------------------

### C#: Fetch Amazon Product Rank Overview Live

Source: https://docs.dataforseo.com/v3/dataforseo_labs/amazon/product_rank_overview/live_bash=

This C# example shows how to use the Dataforseo Labs API to retrieve live Amazon product rank data. It configures an HttpClient with authentication, prepares the POST data including ASINs, location, and language, and deserializes the JSON response, handling potential errors.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_amazon_product_rank_overview_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                asins = new[]

                {

                    "B001TJ3HUG",

                    "B01LW2SL7R"

                },

                location_name = "United States",

                language_name = "English"

            });

            // POST /v3/dataforseo_labs/amazon/product_rank_overview/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/amazon/product_rank_overview/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### API POST Request Example (Python)

Source: https://docs.dataforseo.com/v3/serp/google/organic/task_post

This code snippet shows a basic example of making a POST request to the DataForSEO API endpoint '/v3/serp/google/organic/task_post'. It assumes a 'client' object is already configured and passes the prepared 'post_data'.

```python
# POST /v3/serp/google/organic/task_post
# in addition to 'google' and 'organic' you can also set other search engine and type parameters
# the full list of possible parameters is available in documentation
response = client.post("/v3/serp/google/organic/task_post", post_data)
```

--------------------------------

### Retrieve SERP Data using Node.js

Source: https://docs.dataforseo.com/v3/serp/yahoo/organic/task_get/advanced

This Node.js example utilizes the 'axios' library to make a GET request to the DataForSEO API. It demonstrates how to set up authentication using basic auth with username and password, specify the API endpoint for advanced SERP data, and handle the response or errors.

```javascript
const task_id = '02231256-2604-0066-2000-57133b8fc54e';



const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/yahoo/organic/task_get/advanced/' + task_id,

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get Serp Locations using C# HttpClient

Source: https://docs.dataforseo.com/v3/serp/google/ads_advertisers/locations

This C# example demonstrates how to retrieve SERP locations using HttpClient. It covers setting up the client with authentication headers, making an asynchronous GET request, deserializing the JSON response, and handling potential errors.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_locations()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of locations

            // GET /v3/serp/google/ads_advertisers/locations

            // in addition to 'google' you can also set other search engine

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/serp/google/ads_advertisers");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Keyword ID using C# HttpClient

Source: https://docs.dataforseo.com/v2/cmn_python=

This C# code snippet demonstrates how to fetch a keyword ID using HttpClient from the DataForSEO API. It sets up the HttpClient with the base address and basic authentication using your provided API credentials. The example is within a static method and uses async Task for the HTTP request.

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task cmn_key_id()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))} 
            };

```

--------------------------------

### Post Google Organic Search Task (PHP)

Source: https://docs.dataforseo.com/v3/serp/google/organic/task_post

This PHP script demonstrates how to post tasks to the DataForSEO API using the provided `RestClient.php` class. It shows how to initialize the client with API credentials and then construct an array of task parameters. The examples cover basic task setup with language and location codes, as well as advanced options including priority, tags, pingback URLs, and postback configurations. Error handling for API requests is also included.

```php
// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {

   // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

   $client = new RestClient($api_url, null, 'login', 'password');

} catch (RestClientException $e) {

   echo "n";

   print "HTTP code: {$e->getHttpCode()}n";

   print "Error code: {$e->getCode()}n";

   print "Message: {$e->getMessage()}n";

   print  $e->getTraceAsString();

   echo "n";

   exit();

}

$post_array = array();

// example #1 - a simple way to set a task

// this way requires you to specify a location, a language of search, and a keyword.

$post_array[] = array(

   "language_code" => "en",

   "location_code" => 2840,

   "keyword" => mb_convert_encoding("albert einstein", "UTF-8")

);

// example #2 - a way to set a task with additional parameters

// high priority allows us to complete a task faster, but you will be charged more money.

// after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.

$post_array[] = array(

   "language_name" => "English",

   "location_name" => "United States",

   "keyword" => mb_convert_encoding("albert einstein", "UTF-8"),

   "priority" => 2,

   "tag" => "some_string_123",

   "pingback_url" => 'https://your-server.com/pingscript?id=$id&tag=$tag'

);

// example #3 - an alternative way to set a task

// all the parameters required to set a task are passed via the URL.

// after a task is completed, we will send the results according to the type you specified in the 'postback_data' field to the address you set in the 'postback_url' field.

$post_array[] = array(

   "url" => "https://www.google.co.uk/search?q=albert%20einstein&hl=en&gl=GB&uule=w+CAIQIFISCXXeIa8LoNhHEZkq1d1aOpZS",

   "postback_data" => "html",

   "postback_url" => "https://your-server.com/postbackscript"

);

// this example has a 3 elements, but in the case of large number of tasks - send up to 100 elements per POST request

if (count($post_array) > 0) {

   try {

      // POST /v3/serp/google/organic/task_post

      // in addition to 'google' and 'organic' you can also set other search engine and type parameters

      // the full list of possible parameters is available in documentation

      $result = $client->post('/v3/serp/google/organic/task_post', $post_array);

      print_r($result);

      // do something with post result

   } catch (RestClientException $e) {

      echo "n";

      print "HTTP code: {$e->getHttpCode()}n";

      print "Error code: {$e->getCode()}n";

      print "Message: {$e->getMessage()}n";

      print  $e->getTraceAsString();

      echo "n";

   }

}

$client = null;

?>
```

--------------------------------

### Check App Review Task Readiness with Node.js (axios)

Source: https://docs.dataforseo.com/v3/app_data/apple/app_reviews/tasks_ready

This Node.js example utilizes the 'axios' library to make a GET request to the DataForSEO API for app review tasks. It demonstrates using the 'auth' object for basic authentication and handling the response or errors.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/app_data/apple/app_reviews/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Post Merchant Google Shopping Shops Tasks in Java (Setup)

Source: https://docs.dataforseo.com/v2/merchant

This Java code snippet provides the setup for posting tasks to the merchant Google Shopping shops endpoint of the DataForSeo API. It includes necessary imports for Apache HttpClient and JSON processing. The actual task posting logic would follow this setup.

```java
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.util.*;
public class Demos {
    public static void merchant_google_shopping_shops_tasks_post() throws JSONException, IOException, URISyntaxException {

```

--------------------------------

### Get Google Ads Advertisers Locations List (Node.js)

Source: https://docs.dataforseo.com/v3/serp/google/ads_advertisers/locations

This Node.js example uses the axios library to make a GET request to the DataForSEO API for Google Ads advertiser locations. It includes basic authentication and demonstrates how to access the results from the API response.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/google/ads_advertisers/locations',

    auth: {

        username: 'login',

        password: 'password'

    },

    data: [{

        country: "us"

    }],

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch Ready Tasks using Node.js and Axios

Source: https://docs.dataforseo.com/v3/serp/google/events/tasks_ready

This Node.js example uses the Axios library to make a GET request to the DataForSEO API to retrieve ready tasks. It handles authentication using the 'auth' object and specifies the content type in the headers. The response data is logged to the console.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/google/events/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### C#: Post AI Optimization LLM Scraper Task (Basic and Advanced)

Source: https://docs.dataforseo.com/v3/ai_optimization/chat_gpt/llm_scraper/task_post

This C# code demonstrates how to post tasks to the DataForSeo AI Optimization LLM Scraper API. It shows two examples: a basic task setup specifying language, location, and keyword, and an advanced setup including priority, a tag, and a pingback URL for real-time notifications. The code utilizes Newtonsoft.Json for serialization and HttpClient for making the POST request.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task ai_optimization_llm_scraper_task_post()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))} 
            };

            var postData = new List<object>();

            // example #1 - a simple way to set a task

            // this way requires you to specify a location, a language of search, and a keyword.

            postData.Add(new

            {

                language_code = "en",

                location_code = 2840,

                keyword = "what is chatgpt"

            });

            // example #2 - a way to set a task with additional parameters

            // high priority allows us to complete a task faster, but you will be charged more credits.

            // after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.

            postData.Add(new

            {

                language_name = "English",

                location_name = "United States",

                keyword = "what is chatgpt",

                priority = 2,

                tag = "some_string_123",

                pingback_url = "https://your-server.com/pingscript?id=$id&tag=$tag"

            });

            // POST /v3/ai_optimization/chat_gpt/llm_scraper/task_post

            // in addition to 'chat_gpt' and 'llm_scraper' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/ai_optimization/chat_gpt/llm_scraper/task_post", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get LLM Mentions Locations and Languages (Node.js)

Source: https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/locations_and_languages

This Node.js example uses the axios library to make a GET request to the AI Optimization LLM Mentions API for locations and languages. It demonstrates handling both successful responses and errors.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/ai_optimization/llm_mentions/locations_and_languages',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get Domain Technologies Summary via API (JavaScript)

Source: https://docs.dataforseo.com/v3/domain_analytics/technologies/technologies_summary/live

This JavaScript example uses the axios library to send a POST request to the DataForSEO API for domain technology summaries. It demonstrates how to configure the request with authentication, the API endpoint, and the JSON payload. The example requires replacing 'login' and 'password' with valid API credentials.

```javascript
const post_array = [];

post_array.push({

    "technologies": ["Nginx"],

    "keywords": ["WordPress"],

    "filters": [["country_iso_code", "=", "US"], "and", ["domain_rank", ">", 800]]

});

const axios = require('axios');
axios({

    method: 'post',

    url: 'https://api.dataforseo.com/v3/domain_analytics/technologies/technologies_summary/live',

    auth: {

        username: 'login',

        password: 'password'

    },

    data: post_array,

    headers: {

        'content-type': 'application/json'

    }

}).then(function(response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function(error) {

    console.log(error);

});
```

--------------------------------

### Retrieve User Data using DataForSEO API (C#)

Source: https://docs.dataforseo.com/v3/appendix/user_data

This C# example demonstrates how to authenticate with the DataForSEO API using Basic Authentication, make a GET request to the '/v3/appendix/user_data' endpoint, deserialize the JSON response, and handle success or error based on the 'status_code'.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task appendix_user_data()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get information about current user

            // GET /v3/appendix/user_data

            var response = await httpClient.GetAsync("/v3/appendix/user_data");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Pages by Resource using Node.js

Source: https://docs.dataforseo.com/v3/on_page/page_by_resource_php=

This Node.js example uses the 'axios' library to make a POST request to the Dataforseo API for retrieving pages by resource. It demonstrates setting up the request URL, authentication, and the JSON data payload. Error handling is included for the API call.

```javascript
const post_array = [];



post_array.push({
  "id": "02241700-1535-0216-0000-034137259bc1",
  "url": "https://www.etsy.com/about/jobs.workco2018.js?"
});



const axios = require('axios');


axios({
  method: 'post',
  url: 'https://api.dataforseo.com/v3/on_page/pages_by_resource',
  auth: {
    username: 'login',
    password: 'password'
  },
  data: post_array,
  headers: {
    'content-type': 'application/json'
  }
}).then(function (response) {
  var result = response['data']['tasks'];
  // Result data
  console.log(result);
}).catch(function (error) {
  console.log(error);
});
```

--------------------------------

### Post Google Product Info Task via JavaScript (Node.js)

Source: https://docs.dataforseo.com/v3/merchant/google/product_info/task_post

This JavaScript example uses the axios library to make a POST request to the DataforSEO API for Google product information. It demonstrates setting up task parameters, including optional fields like priority and pingback URL, and handles authentication using basic auth. The response and potential errors are logged to the console.

```javascript
const post_array = [];



post_array.push({

  "location_name": "United States",

  "language_name": "English",

  "product_id": "1113158713975221117",

  "priority": 2,

  "tag": "some_string_123",

  "pingback_url": 'https://your-server.com/pingscript?id=$id&tag=$tag'

});



const axios = require('axios');



axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/merchant/google/product_info/task_post',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);



}).catch(function (error) {

  console.log(error);



});
```

--------------------------------

### PHP: Get Keyword Finder Locations using RestClient

Source: https://docs.dataforseo.com/v2/cmn_python=

This snippet demonstrates how to fetch keyword finder location data using the PHP RestClient. It requires the RestClient.php file and API credentials. The function makes a GET request to the 'v2/cmn_locations_stat_kwrd_finder' endpoint and prints the results or error details.

```php
<?php
require('RestClient.php');
//You can download this file from here https://api.dataforseo.com/_examples/php/_php_RestClient.zip
try {
    //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
    $client = new RestClient('https://api.dataforseo.com/', null, 'login', 'password');
    $status_result = $client->get('v2/cmn_locations_stat_kwrd_finder');
    print_r($status_result);
    //do something with the result
} catch (RestClientException $e) {
    echo "\n";
    print "HTTP code: {$e->getHttpCode()}\n";
    print "Error code: {$e->getCode()}\n";
    print "Message: {$e->getMessage()}\n";
    print  $e->getTraceAsString();
    echo "\n";
    exit();
}
$client = null;
?>
```

```php
<?php
require('RestClient.php');
//You can download this file from here https://api.dataforseo.com/_examples/php/_php_RestClient.zip

try {
    //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
    $client = new RestClient('https://api.dataforseo.com/', null, 'login', 'password');

    $status_result = $client->get('v2/cmn_locations_stat_kwrd_finder');
    print_r($status_result);

    //do something with the result

} catch (RestClientException $e) {
    echo "\n";
    print "HTTP code: {$e->getHttpCode()}\n";
    print "Error code: {$e->getCode()}\n";
    print "Message: {$e->getMessage()}\n";
    print  $e->getTraceAsString();
    echo "\n";
    exit();
}

$client = null;
?>
```

```php
<?php
require('RestClient.php');
//You can download this file from here https://api.dataforseo.com/_examples/php/_php_RestClient.zip

try {
    //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
    $client = new RestClient('https://api.dataforseo.com/', null, 'login', 'password');

    $status_result = $client->get('v2/cmn_locations_stat_kwrd_finder');
    print_r($status_result);

    //do something with the result

} catch (RestClientException $e) {
    echo "\n";
    print "HTTP code: {$e->getHttpCode()}\n";
    print "Error code: {$e->getCode()}\n";
    print "Message: {$e->getMessage()}\n";
    print  $e->getTraceAsString();
    echo "\n";
    exit();
}

$client = null;
?>
```

--------------------------------

### API Request Examples (cURL, PHP, Node.js, Python, C#)

Source: https://docs.dataforseo.com/v3/ai_optimization/llm_mentions/filters

Provides a template for constructing API requests using cURL, PHP, Node.js, Python, and C#. These examples illustrate how to interact with DataForSEO endpoints and incorporate filtering parameters.

```more
cURL

```

```more
php

```

```more
Node.js

```

```more
Python

```

```more
cSharp

```

--------------------------------

### Fetch Google SERP Locations using Python

Source: https://docs.dataforseo.com/v3/serp/google/locations

This Python example utilizes the provided RestClient to retrieve a list of Google SERP locations. It requires downloading the python_Client.zip and includes basic usage for making the GET request. Ensure your login and password are correct.

```python
from random import Random
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip



client = RestClient("login", "password")
# using this method you can get a list of locations
# GET /v3/serp/google/locations
# in addition to 'google' you can also set other search engine
# the full list of possible parameters is available in documentation
response = client.get("/v3/serp/google/locations")

```

--------------------------------

### Content Generation API Initialization using Python

Source: https://docs.dataforseo.com/v3/content_generation/generate/live

This Python snippet shows the initialization of the RestClient for interacting with the DataForSEO API. It sets up the client with login and password credentials and prepares a dictionary for the POST request data, which would then be used for making the API call.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()

```

--------------------------------

### Fetch YouTube Organic Tasks (Node.js)

Source: https://docs.dataforseo.com/v3/serp/youtube/organic/tasks_fixed

This Node.js example uses the `axios` library to make a GET request to the DataForSEO API. It demonstrates how to set up authentication using basic auth with username and password, and specify the content type. The response data, specifically the 'result' from the first task, is then logged to the console.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/youtube/organic/tasks_fixed',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch AI Optimization Models and SERP Languages (PHP)

Source: https://docs.dataforseo.com/v3/ai_optimization/perplexity/llm_responses/models

Demonstrates how to use the RestClient library in PHP to interact with the DataForSeo API. It shows how to authenticate and make GET requests to fetch AI models and SERP languages. Includes error handling for API requests.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {

    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

    $client = new RestClient($api_url, null, 'login', 'password');

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

    exit();

}

try {

    // using this method you can get a list of ai models

    // GET /v3/ai_optimization/perplexity/llm_responses/models

    // the full list of possible parameters is available in documentation

    $result = $client->get('/v3/serp/google/ai_mode/languages');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### Retrieve User Data using C#

Source: https://docs.dataforseo.com/v2/cmn

This C# example demonstrates fetching user data via the DataForSeo API using HttpClient. It requires Newtonsoft.Json for JSON deserialization and basic .NET libraries. Replace 'login' and 'password' with your API credentials. The code sends a GET request and handles both successful responses and errors.

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task cmn_user()
        {
            var httpClient = new HttpClient {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };
            var response = await httpClient.GetAsync("v2/cmn_user");
            var obj = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());
            if (obj.status == "error")
                Console.WriteLine($"error. Code: {obj.error.code} Message: {obj.error.message}");
            else
                
```

--------------------------------

### Post Yahoo Organic Task via JavaScript (Node.js)

Source: https://docs.dataforseo.com/v3/serp/yahoo/organic/task_post_php=

This Node.js example uses the 'axios' library to post tasks for Yahoo organic search results. It demonstrates how to configure the request with authentication, headers, and a JSON data payload containing task parameters. Ensure you have 'axios' installed (`npm install axios`).

```javascript
const post_array = [];



post_array.push({

  "language_name": "English",

  "location_name": "United States",

  "keyword": encodeURI("albert einstein")

});



const axios = require('axios');



axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/serp/yahoo/organic/task_post',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Make API Request and Handle Response (C#)

Source: https://docs.dataforseo.com/v3/app_data/apple/app_list/tasks_ready

This C# example demonstrates making an asynchronous GET request to the DataForSEO API using HttpClient. It deserializes the JSON response, checks the 'status_code', and prints either the result or an error message. Authentication is handled via a Basic Header.

```csharp
using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task app_data_apple_app_list_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/app_data/apple/app_list/tasks_ready

            var response = await httpClient.GetAsync("/v3/app_data/apple/app_list/tasks_ready");

            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Post Google SERP Search by Image Task (C#)

Source: https://docs.dataforseo.com/v3/serp/google/search_by_image/task_post

This C# code example demonstrates how to use the DataForSeo API to post a task for a Google SERP search by image. It includes examples of setting basic parameters like language, location, and image URL, as well as advanced parameters like priority, tag, and pingback URL. The code handles the API response and prints success or error messages.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;

namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_task_post()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            // example #1 - a simple way to set a task

            // this way requires you to specify a location, a language of search, and a image_url.

            postData.Add(new

            {

                language_code = "en",

                location_code = 2840,

                image_url = "https://dataforseo.com/wp-content/uploads/2016/11/data_for_seo_light_429.png"

            });

            // example #2 - a way to set a task with additional parameters

            // high priority allows us to complete a task faster, but you will be charged more credits.

            // after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.

            postData.Add(new

            {

                language_name = "English",

                location_name = "United States",

                image_url = "https://dataforseo.com/wp-content/uploads/2016/11/data_for_seo_light_429.png",

                priority = 2,

                tag = "some_string_123",

                pingback_url = "https://your-server.com/pingscript?id=$id&tag=$tag"

            });

            // POST /v3/serp/google/search_by_image/task_post

            // in addition to 'google' and 'search_by_image' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/serp/google/search_by_image/task_post", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Domain Page Summary using Node.js

Source: https://docs.dataforseo.com/v3/backlinks/domain_pages_summary/live

This Node.js example uses the 'axios' library to make a POST request to the DataForSEO API for domain page summaries. It demonstrates setting up the request with authentication, URL, headers, and the JSON payload.

```javascript
const post_array = [];



post_array.push({

  "target": "forbes.com",

  "limit": 4,

  "order_by": ["backlinks,desc"]

});



const axios = require('axios');



axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/backlinks/domain_pages_summary/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});


```

--------------------------------

### Get Google Jobs Locations List (C#)

Source: https://docs.dataforseo.com/v3/serp/google/jobs/locations

This C# example demonstrates how to use HttpClient to make a GET request to the DataForSEO API for Google Jobs locations. It includes setting up authentication headers and deserializing the JSON response, with error handling.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_locations()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))
}

            };

            // using this method you can get a list of locations

            // GET /v3/serp/google/jobs/locations

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/serp/google/jobs/locations");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Fetch Completed Tasks using JavaScript (Node.js)

Source: https://docs.dataforseo.com/v3/business_data/trustpilot/search/tasks_ready

This JavaScript example utilizes the axios library to make a GET request to the /v3/business_data/trustpilot/search/tasks_ready endpoint. It demonstrates using the `auth` object for credentials and handling the response or errors.

```javascript
const axios = require('axios');

axios({
    method: 'get',
    url: 'https://api.dataforseo.com/v3/business_data/trustpilot/search/tasks_ready',
    auth: {
        username: 'login',
        password: 'password'
    },
    headers: {
        'content-type': 'application/json'
    }
}).then(function (response) {
    var result = response['data']['tasks'][0]['result'];
    // Result data
    console.log(result);
}).catch(function (error) {
    console.log(error);
});
```

--------------------------------

### Fetch Apple App List Tasks Ready (JavaScript)

Source: https://docs.dataforseo.com/v3/app_data/apple/app_list/tasks_ready

This JavaScript example uses the `axios` library to make a GET request to the DataForSEO API for Apple app data tasks. It handles the response and potential errors, logging the results to the console.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/app_data/apple/app_list/tasks_ready',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Fetch Google Ads Advertisers Tasks Ready with PHP

Source: https://docs.dataforseo.com/v3/serp/google/ads_advertisers/tasks_ready

This PHP example demonstrates how to fetch completed tasks for Google Ads advertisers using the RestClient library. It initializes the client with API credentials and makes a GET request to the 'tasks_ready' endpoint. Error handling for API requests is included.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

try {

    // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

    $client = new RestClient($api_url, null, 'login', 'password');

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

    exit();

}

try {

    // using this method you can get a list of completed tasks

    // GET /v3/serp/google/ads_advertisers/tasks_ready

    // in addition to 'google' and 'ads_advertisers' you can also set other search engine and type parameters

    // the full list of possible parameters is available in documentation

    $result = $client->get('/v3/serp/google/ads_advertisers/tasks_ready');

    print_r($result);

    // do something with result

} catch (RestClientException $e) {

    echo "n";

    print "HTTP code: {$e->getHttpCode()}n";

    print "Error code: {$e->getCode()}n";

    print "Message: {$e->getMessage()}n";

    print  $e->getTraceAsString();

    echo "n";

}

$client = null;

?>
```

--------------------------------

### JavaScript (Node.js): Fetch Google Keywords Data with Axios

Source: https://docs.dataforseo.com/v3/keywords_data/google/keywords_for_site/task_post

This JavaScript example uses the Axios library to make a POST request to the DataForSEO API for Google keywords data. It demonstrates how to configure the request with authentication (using 'username' and 'password' for basic auth), set the request body with task parameters, and handle the response or errors. Ensure your Node.js environment has Axios installed (`npm install axios`).

```javascript
const post_array = [];



post_array.push({

  "language_code": "en",

  "location_code": 2840,

  "target": "dataforseo.com",

  "tag": "some_string_123",

});



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/keywords_data/google/keywords_for_site/task_post',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Fetch Pinterest Live Data via Node.js Axios

Source: https://docs.dataforseo.com/v3/business_data/social_media/pinterest/live

This JavaScript example uses the Axios library to make a POST request to the DataForSEO API for live Pinterest data. It demonstrates setting up authentication via the `auth` object and sending the target data in the request body. The response and any errors are logged to the console.

```javascript
const post_array = [];



post_array.push({

  "tag": "some_string_123",

  "targets": ["https://www.simplyrecipes.com/recipes/grilled_salmon_with_cucumber_mango_salsa/", "https://tasty.co/recipe/classic-lasagna", "https://www.allrecipes.com/recipe/255263/sicilian-roasted-chicken/"]

});



const axios = require('axios');



axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/business_data/social_media/pinterest/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Get Current User Information (API)

Source: https://docs.dataforseo.com/v2/cmn_java=

This API endpoint, `GET https://api.dataforseo.com/v2/cmn_user`, retrieves information about the current authenticated user. The response is a JSON object containing a `results` array with user details. It includes status indicators and error reporting for failed requests.

```http
GET https://api.dataforseo.com/v2/cmn_user
```

```json
{
    "status": "string",
    "error": [
        {
            "code": "integer",
            "message": "string"
        }
    ],
    "results": [
        // User information objects here
    ]
}
```

--------------------------------

### Dataforseo API Filters Example

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live_php=

Demonstrates how to use the 'filters' parameter to refine API results. It shows examples of applying comparison operators, logical operators (AND/OR), and nested filter conditions.

```json
["keyword_info.search_volume",">",0]
[["keyword_info.search_volume","in",[0,1000]], "and", ["keyword_info.competition_level","=","LOW"]]
[["keyword_info.search_volume",">",100], "and", [["keyword_info.cpc","<",0.5], "or", ["keyword_info.high_top_of_page_bid","<=",0.5]]]
```

--------------------------------

### Fetch Google Search Tasks Ready (Bash)

Source: https://docs.dataforseo.com/v3/serp/google/search_by_image/tasks_ready

This Bash script demonstrates how to authenticate with the DataForSEO API using basic authentication and fetch a list of ready Google search tasks. It encodes the login and password using base64 for the Authorization header.

```bash
login="login"

password="password"

cred="$(printf ${login}:${password} | base64)"

curl --location --request GET "https://api.dataforseo.com/v3/serp/google/search_by_image/tasks_ready" \

--header "Authorization: Basic ${cred}"  \

--header "Content-Type: application/json" \

--data-raw ""
```

--------------------------------

### Get cmn_adwords_status using Java

Source: https://docs.dataforseo.com/v2/cmn_python=

This Java code snippet demonstrates how to retrieve the Google Ads status relevance using the DataforSEO API. It utilizes Apache HttpClient for making the GET request and includes basic authentication. The response is parsed as a JSON object to check for errors or display results.

```java
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.util.*;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;

public class Demos {
    public static void cmn_adwords_status() throws JSONException, IOException {
        HttpClient client;
        client = HttpClientBuilder.create().build();
        HttpGet get = new HttpGet("https://api.dataforseo.com/v2/cmn_adwords_status");
        //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
        String basicAuth = Base64.getEncoder().encodeToString(("login:password").getBytes("UTF-8"));

        get.setHeader("Content-type", "application/json");
        get.setHeader("Authorization", "Basic " + basicAuth);
        HttpResponse response = client.execute(get);
        JSONObject obj = new JSONObject(EntityUtils.toString(response.getEntity()));

        if (obj.get("status").equals("error")) {
            System.out.println("error. Code:" + obj.getJSONObject("error").get("code") + " Message: " + obj.getJSONObject("error").get("message"));
        } else {
            JSONArray results = obj.getJSONArray("results");
            if (results.length() > 0) {
                for (int i = 0; i < results.length(); i++) {
                    System.out.println(results.get(i));
                }
            } else {
                System.out.println("no results");
            }
        }
    }
}
```

--------------------------------

### C# API Request Example (Conceptual)

Source: https://docs.dataforseo.com/v3/databases/amazon/products

Presents a conceptual API request example in C#. This snippet illustrates how to construct and send HTTP requests to DataForSEO APIs using HttpClient, including setting necessary headers.

```csharp
// Conceptual C# example (specific endpoint and parameters required)
using System;
using System.Net.Http;
using System.Threading.Tasks;

public class DataForSeoApiHelper
{
    public static async Task CallApiAsync()
    {
        string apiKey = "YOUR_API_KEY";
        string url = "https://api.dataforseo.com/v3/serp/google/organic/live?keyword=example";

        using (var client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
            client.DefaultRequestHeaders.Add("Content-Type", "application/json");

            try
            {
                HttpResponseMessage response = await client.GetAsync(url);
                response.EnsureSuccessStatusCode(); // Throw if not 2xx

                string responseBody = await response.Content.ReadAsStringAsync();
                Console.WriteLine(responseBody);
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Request error: {e.Message}");
            }
        }
    }
}
```

--------------------------------

### Fetch Google Keywords Data (C#)

Source: https://docs.dataforseo.com/v3/keywords_data/google/keywords_for_keywords/live_php=

This C# code example demonstrates how to fetch Google keywords data using the DataForSeo API. It sets up an HTTP client, constructs a POST request with keywords, location, and language, and then processes the JSON response. It includes error handling based on the status code.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_keywords_for_keywords_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(

                new

                {

                    location_name = "United States",

                    language_name = "English",

                    keywords = new[]

                        {

                            "average page rpm adsense",

                            "adsense blank ads how long",

                            "leads and prospects"

                        }

                });

            // POST /v3/keywords_data/google/keywords_for_keywords/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/keywords_data/google/keywords_for_keywords/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}
```

--------------------------------

### GET /v3/serp/bing/languages

Source: https://docs.dataforseo.com/v3/serp/bing/languages

Retrieves a list of supported languages for the specified search engine. Currently, 'bing' is shown as an example, but other search engines can be specified.

```APIDOC
## GET /v3/serp/bing/languages

### Description
Retrieves a list of supported languages for the specified search engine. This endpoint is useful for understanding localization options for SERP data collection.

### Method
GET

### Endpoint
/v3/serp/bing/languages

### Parameters
#### Query Parameters
- **engine** (string) - Optional - The search engine for which to retrieve the list of languages. Defaults to 'bing'. Other possible values include 'google', 'yahoo', etc. (refer to documentation for a full list).

### Request Example
This endpoint does not typically require a request body.

### Response
#### Success Response (200)
- **status_code** (integer) - The status code of the operation. 20000 indicates success.
- **status_message** (string) - A message indicating the status of the operation.
- **time** (string) - The time taken to process the request.
- **cost** (number) - The cost of the API call.
- **data** (object) - Contains the list of languages.
  - **languages** (array) - A list of language objects.
    - **name** (string) - The name of the language.
    - **code** (string) - The code representing the language.

#### Response Example
```json
{
    "version": "3.20191128",
    "status_code": 20000,
    "status_message": "OK.",
    "time": "0.131",
    "cost": 0.00123,
    "data": {
        "languages": [
            {
                "name": "English",
                "code": "en"
            },
            {
                "name": "Spanish",
                "code": "es"
            }
        ]
    }
}
```

#### Error Handling
- **status_code** (integer) - Non-20000 codes indicate an error. Refer to the appendix for a full list of error codes and messages. Common errors include authentication failures, invalid parameters, or rate limiting.

- **status_message** (string) - A message describing the error.

- **time** (string) - The time taken to process the request.

- **cost** (number) - The cost of the API call.

### Example Usage (C#)
```csharp
using Newtonsoft.Json;
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task serp_languages()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) } // Replace with your credentials
            };

            var response = await httpClient.GetAsync("/v3/serp/bing/languages");
            var result = JsonConvert.DeserializeObject<dynamic>(await response.Content.ReadAsStringAsync());

            if (result.status_code == 20000)
            {
                Console.WriteLine(JsonConvert.SerializeObject(result.data, Formatting.Indented));
            }
            else
            {
                Console.WriteLine($"Error. Code: {result.status_code} Message: {result.status_message}");
            }
        }
    }
}
```
```

--------------------------------

### Submit SERP Task via POST Request (C#)

Source: https://docs.dataforseo.com/v3/serp/google/images/task_post

This C# code example shows how to post a task to the DataForSEO API using HttpClient. It includes setting up authorization, constructing the post data with various parameter options, sending the request, and deserializing the JSON response. The example highlights different ways to specify task parameters like location, language, and keywords.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_task_post()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))

                }

            };

            var postData = new List<object>();

            // example #1 - a simple way to set a task

            // this way requires you to specify a location, a language of search, and a keyword.

            postData.Add(new

            {

                language_code = "en",

                location_code = 2840,

                keyword = "albert einstein"

            });

            // example #2 - a way to set a task with additional parameters

            // high priority allows us to complete a task faster, but you will be charged more credits.

            // after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.

            postData.Add(new

            {

                language_name = "English",

                location_name = "United States",

                keyword = "albert einstein",

                priority = 2,

                tag = "some_string_123",

                pingback_url = "https://your-server.com/pingscript?id=$id&tag=$tag"

            });

            // example #3 - an alternative way to set a task

            // all the parameters required to set a task are passed via the URL.

            // after a task is completed, we will send the results according to the type you specified in the 'postback_data' field to the address you set in the 'postback_url' field.

            postData.Add(new

            {

                url = "https://www.google.co.uk/search?q=albert%20einstein&hl=en&gl=GB&uule=w+CAIQIFISCXXeIa8LoNhHEZkq1d1aOpZS",

                postback_data = "html",

                postback_url = "https://your-server.com/postbackscript"

            });

            // POST /v3/serp/google/images/task_post

            // in addition to 'google' and 'images' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/serp/google/images/task_post", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### GET /v2/cmn_user

Source: https://docs.dataforseo.com/v2/cmn_java=

Retrieves user information, such as account details and usage statistics. Requires Basic Authentication with your DataForSEO API credentials.

```APIDOC
## GET /v2/cmn_user

### Description
This endpoint retrieves account-specific user information. It is useful for checking your account status, available credits, and other relevant details.

### Method
GET

### Endpoint
https://api.dataforseo.com/v2/cmn_user

### Parameters
#### Query Parameters
None

#### Path Parameters
None

#### Request Body
None

### Request Example
```bash
curl -X GET "https://api.dataforseo.com/v2/cmn_user" \
     -H "Authorization: Basic YOUR_BASE64_ENCODED_CREDENTIALS"
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the API request (e.g., "ok").
- **results** (array) - An array containing user information objects.
  - **user_utc_offset** (string) - The user's time zone offset in UTC.
  - **account_id** (integer) - The unique identifier for the user's account.
  - **is_paid_account** (boolean) - A flag indicating if the account is a paid account.
  - **daily_task_limit** (integer) - The daily limit for tasks.
  - **daily_tasks_left** (integer) - The number of tasks remaining for the day.
  - **monthly_task_limit** (integer) - The monthly limit for tasks.
  - **monthly_tasks_left** (integer) - The number of tasks remaining for the month.
  - **free_tasks_left** (integer) - The number of free tasks remaining.

#### Response Example
```json
{
    "status": "ok",
    "results": [
        {
            "user_utc_offset": "+00:00",
            "account_id": 123456,
            "is_paid_account": true,
            "daily_task_limit": 5000,
            "daily_tasks_left": 4980,
            "monthly_task_limit": 150000,
            "monthly_tasks_left": 149000,
            "free_tasks_left": 0
        }
    ]
}
```

#### Error Response (401)
- **status** (string) - Indicates the status of the API request (e.g., "error").
- **error** (object) - Contains error details.
  - **code** (integer) - The error code.
  - **message** (string) - A description of the error.
  - **timestamp** (string) - The time the error occurred.

#### Error Response Example
```json
{
    "status": "error",
    "error": {
        "code": 7,
        "message": "authorization was not provided",
        "timestamp": "2023-10-27 10:00:00"
    }
}
```
```

--------------------------------

### Post Request for Bing Keyword Suggestions (C#)

Source: https://docs.dataforseo.com/v3/keywords_data/bing/keyword_suggestions_for_url/task_post

This C# example demonstrates how to make a POST request to the DataForSEO API for Bing keyword suggestions. It includes setting up the HttpClient, authentication, constructing the request payload using Newtonsoft.Json, sending the request, and deserializing the response. It also includes error handling based on the status code.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task keywords_data_bing_keyword_suggestions_for_url_task_post()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                target = "https://dataforseo.com/apis/serp-api"

            });

            // POST /v3/keywords_data/bing/keyword_suggestions_for_url/task_post

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/keywords_data/bing/keyword_suggestions_for_url/task_post", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Keyword ID

Source: https://docs.dataforseo.com/v2/cmn_python=

This endpoint allows you to retrieve a unique ID for a given keyword. It's essential for various SEO-related operations within the DataForSEO platform.

```APIDOC
## GET /v2/cmn_key_id/{keyword}

### Description
Retrieves a unique ID for a specified keyword.

### Method
GET

### Endpoint
/v2/cmn_key_id/{keyword}

#### Path Parameters
- **keyword** (string) - Required - The keyword for which to retrieve the ID.

### Request Example
```bash
GET /v2/cmn_key_id/online%20rank%20checker
```

### Response
#### Success Response (200)
- **results** (array) - An array containing keyword information.
  - **key_id** (string) - The unique identifier for the keyword.

#### Response Example
```json
{
  "status": "ok",
  "results": [
    {
      "keyword": "online rank checker",
      "key_id": "some_key_id_value"
    }
  ]
}
```

#### Error Handling
- **error** (object) - Contains error details if the request fails.
  - **code** (integer) - The error code.
  - **message** (string) - A description of the error.

#### Error Response Example
```json
{
  "status": "error",
  "error": {
    "code": 400,
    "message": "Invalid parameter"
  }
}
```
```

--------------------------------

### Fetch Trustpilot Reviews Tasks Ready using Python RestClient

Source: https://docs.dataforseo.com/v3/business_data/trustpilot/reviews/tasks_ready

This Python snippet demonstrates fetching Trustpilot reviews tasks ready using the provided RestClient. It requires downloading the python_Client.zip file and initializes the client with your login and password. Replace 'login' and 'password' with your actual API credentials.

```python
from client import RestClient

# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip

client = RestClient("login", "password")

# using this method you can get a list of completed tasks

# GET /v3/business_data/trustpilot/reviews/tasks_ready

response = client.get("/v3/business_data/trustpilot/reviews/tasks_ready")
```

--------------------------------

### DataforSEO API Access Example (PHP)

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live

This PHP code example shows how to authenticate and make requests to the DataforSEO API. It emphasizes using your registered API credentials for successful authorization. Ensure you have the necessary libraries for making HTTP requests.

```php
<?php

// Instead of ‘login’ and ‘password’ use your credentials from https://app.dataforseo.com/api-access

$credentials = base64_encode('login:password');
$context = stream_context_create([
    'http' => [
        'header' => "Authorization: Basic {$credentials}"
    ]
]);

$content = file_get_contents('https://api.dataforseo.com/v3/...', false, $context);
var_dump(json_decode($content, true));

?>
```

--------------------------------

### Fetch Google My Business Updates Tasks Ready (C#)

Source: https://docs.dataforseo.com/v3/business_data/google/my_business_updates/tasks_ready

This C# code example shows how to use the HttpClient to make a GET request to the /v3/business_data/google/my_business_updates/tasks_ready endpoint. It authenticates using Basic HTTP authentication and deserializes the JSON response. The code then checks the status code and prints either the result or an error message, providing a practical implementation for retrieving task statuses.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task business_data_updates_tasks_ready()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of completed tasks

            // GET /v3/business_data/google/my_business_updates/tasks_ready

            var response = await httpClient.GetAsync("/v3/business_data/google/my_business_updates/tasks_ready");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### PHP Example for Fetching Task Results

Source: https://docs.dataforseo.com/v3/serp/yahoo/organic/task_get/advanced_bash=

PHP code demonstrating how to fetch completed tasks and their results using the DataForSEO API.

```APIDOC
## PHP Example for Fetching Task Results

### Description
This PHP script demonstrates how to retrieve a list of completed tasks and then fetch the detailed results for each task using the DataForSEO API. It includes error handling for API requests.

### Method
GET

### Endpoint
Multiple endpoints used: `/v3/serp/yahoo/organic/tasks_ready` and `/v3/serp/yahoo/organic/task_get/advanced/$id`

### Parameters
**Credentials**: Replace 'login' and 'password' with your actual API credentials from https://app.dataforseo.com/api-access.

### Request Example (PHP)
```php
<?php

// Ensure you have the RestClient.php file included (download from https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip)
require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';
$login = 'your_login'; // Replace with your login
$password = 'your_password'; // Replace with your password

try {
    $client = new RestClient($api_url, null, $login, $password);
} catch (RestClientException $e) {
    echo "n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "n";
    exit();
}

try {
    $result = array();

    // Get a list of completed tasks
    $tasks_ready = $client->get('/v3/serp/yahoo/organic/tasks_ready');

    if (isset($tasks_ready['status_code']) && $tasks_ready['status_code'] === 20000) {
        foreach ($tasks_ready['tasks'] as $task) {
            if (isset($task['result'])) {
                foreach ($task['result'] as $task_ready) {
                    // Get results of each completed task by endpoint
                    if (isset($task_ready['endpoint_advanced'])) {
                        $result[] = $client->get($task_ready['endpoint_advanced']);
                    }
                    // Alternatively, get results by task ID
                    /*
                    if (isset($task_ready['id'])) {
                        $result[] = $client->get('/v3/serp/yahoo/organic/task_get/advanced/' . $task_ready['id']);
                    }
                    */
                }
            }
        }
    }

    print_r($result);

} catch (RestClientException $e) {
    echo "n";
    print "HTTP code: {$e->getHttpCode()}n";
    print "Error code: {$e->getCode()}n";
    print "Message: {$e->getMessage()}n";
    print  $e->getTraceAsString();
    echo "n";
}

$client = null;

?>
```

### Response
#### Success Response (200)
- **tasks** (array) - An array containing the results of completed tasks.

#### Response Example (JSON)
```json
[
  {
    "tasks": [
      {
        "task_processes": [
          {
            "id": "02231256-2604-0066-2000-57133b8fc54e",
            "status_code": 200,
            "status_message": "Ok.",
            "time_taken": 0.123
          }
        ],
        "se_results": [
          {
             "references": [
                {
                  "type": "ai_overview_reference",
                  "source": "Example Domain",
                  "domain": "example.com",
                  "url": "https://example.com",
                  "title": "Example Title",
                  "text": "Sample text snippet.",
                  "rectangle": {
                    "x": 5.0,
                    "y": 10.0,
                    "width": 100.0,
                    "height": 50.0
                  }
                }
              ]
          }
        ]
      }
    ]
  }
]
```
```

--------------------------------

### GET /v2/cmn_key_id

Source: https://docs.dataforseo.com/v2/cmn_csharp=

Retrieves a common keyword ID based on a provided keyword. This endpoint is useful for obtaining unique identifiers for keywords that can be used in other API requests.

```APIDOC
## GET /v2/cmn_key_id

### Description
Retrieves a common keyword ID based on a provided keyword. This endpoint is useful for obtaining unique identifiers for keywords that can be used in other API requests.

### Method
GET

### Endpoint
/v2/cmn_key_id/{keyword}

### Parameters
#### Path Parameters
- **keyword** (string) - Required - The keyword for which to retrieve the ID.

### Request Example
```bash
curl -X GET https://api.dataforseo.com/v2/cmn_key_id/online%20rank%20checker \
     -H "Authorization: Basic YOUR_BASE64_ENCODED_CREDENTIALS"
```

### Response
#### Success Response (200)
- **status** (string) - Indicates the status of the request (e.g., "ok").
- **results** (array) - An array containing keyword ID information.
  - **key_id** (integer) - The common keyword ID.

#### Response Example
```json
{
    "status": "ok",
    "results": [
        {
            "key_id": 123456789
        }
    ]
}
```

#### Error Response (e.g., 400, 401, 403, 404, 500)
- **status** (string) - Indicates the status of the request (e.g., "error").
- **error** (object) - Contains error details.
  - **code** (integer) - The error code.
  - **message** (string) - A message describing the error.

#### Error Response Example
```json
{
    "status": "error",
    "error": {
        "code": 400,
        "message": "Bad Request"
    }
}
```
```

--------------------------------

### Fetch Google SERP Dataset Info using Python

Source: https://docs.dataforseo.com/v3/serp/google/dataset_info/tasks_fixed

This Python example uses a custom RestClient to fetch Google SERP dataset information. It requires downloading the python_Client.zip and extracting RestClient.py. The snippet initializes the client with credentials and makes a GET request to the specified API endpoint, printing the response.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip

client = RestClient("login", "password")

# using this method you can get a list of completed tasks

# GET /v3/serp/google/dataset_info/tasks_fixed

# in addition to 'google' and 'dataset_info' you can also set other search engine and type parameters

# the full list of possible parameters is available in documentation

response = client.get("/v3/serp/google/dataset_info/tasks_fixed")
```

--------------------------------

### Get Google Seller Ad URL using C#

Source: https://docs.dataforseo.com/v3/merchant/google/sellers/ad_url

This C# example shows how to retrieve a Google seller's ad URL via the DataForSeo API. It uses HttpClient for making asynchronous GET requests to the /v3/merchant/google/sellers/ad_url/ endpoint, with Basic authentication. The code deserializes the JSON response and includes logic to process task results or report errors.

```csharp
using Newtonsoft.Json;
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task merchant_google_sellers_ad_url()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }
            };

            // get ad_url by the ad_aclk
            // GET /v3/merchant/google/sellers/ad_url/$ad_aclk
            // use the ad_aclk that you received upon a sellers task
            string ad_aclk = "DChcSEwiSl5TKpbPoAhVFmdUKHfa_B_wYABADGgJ3cw&sig";

            var taskGetResponse = await httpClient.GetAsync("/v3/merchant/google/sellers/ad_url/" + ad_aclk);
            var result = JsonConvert.DeserializeObject(await taskGetResponse.Content.ReadAsStringAsync());

            if (result.tasks != null)
            {
                foreach (var taskResult in result.tasks)
                {
                    var fst = taskResult.First;
                    // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
                    if (fst.status_code >= 40000 || fst.result == null)
                        Console.WriteLine($"error. Code: {fst.status_code} Message: {fst.status_message}");
                    else
                        // do something with result
                        Console.WriteLine(String.Join(Environment.NewLine, fst));
                }
            }
            else
                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");
        }
    }
}

```

--------------------------------

### Get Merchant Amazon Sellers Tasks Ready (Python)

Source: https://docs.dataforseo.com/v3/merchant/amazon/sellers/tasks_ready

This Python example uses a provided RestClient to query the Dataforseo API for completed merchant Amazon seller tasks. It requires the client to be initialized with login credentials.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
# using this method you can get a list of completed tasks
# GET /v3/merchant/amazon/sellers/tasks_ready
response = client.get("/v3/merchant/amazon/sellers/tasks_ready")
```

--------------------------------

### Get Google Bulk Keyword Difficulty using Node.js

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live

This Node.js example utilizes the axios library to send a POST request to the Dataforseo Labs Google Bulk Keyword Difficulty API. It shows how to configure the request with the API endpoint, authentication credentials, and the JSON data payload containing keywords, language, and location. The example includes basic success and error handling for the API response.

```javascript
const post_array = [];



post_array.push({

  "keywords": [

    "dentist new york",

    "pizza brooklyn",

    "car dealer los angeles"

  ],

  "language_name": "English",

  "location_code": 2840

});



const axios = require('axios');


axios({

  method: 'post',

  url: 'https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live',

  auth: {

    username: 'login',

    password: 'password'

  },

  data: post_array,

  headers: {

    'content-type': 'application/json'

  }

}).then(function (response) {

  var result = response['data']['tasks'];

  // Result data

  console.log(result);

}).catch(function (error) {

  console.log(error);

});
```

--------------------------------

### Get Completed Amazon ASIN Tasks - PHP

Source: https://docs.dataforseo.com/v3/merchant/amazon/asin/tasks_ready_php=

This PHP code snippet shows how to fetch completed Amazon ASIN tasks using the Dataforseo RestClient. It requires the `RestClient.php` library and initializes the client with API credentials. The example demonstrates making a GET request to the '/v3/merchant/amazon/asin/tasks_ready' endpoint and includes error handling for API exceptions.

```php
<?php

// You can download this file from here https://cdn.dataforseo.com/v3/examples/php/php_RestClient.zip

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');



try {

   // using this method you can get a list of completed tasks

   // GET /v3/merchant/amazon/asin/tasks_ready

   $result = $client->get('/v3/merchant/amazon/asin/tasks_ready');

   print_r($result);

   // do something with result

} catch (RestClientException $e) {

   echo "n";

   print "HTTP code: {$e->getHttpCode()}n";

   print "Error code: {$e->getCode()}n";

   print "Message: {$e->getMessage()}n";

   print  $e->getTraceAsString();

   echo "n";

}

$client = null;

?>
```

--------------------------------

### Perform Live Business Listing Search (C#)

Source: https://docs.dataforseo.com/v3/business_data/business_listings/search/live

This C# code snippet shows how to perform a live search for business listings using the DataForSeo API. It utilizes `HttpClient` and `Newtonsoft.Json` to make a POST request to the `/v3/business_data/business_listings/search/live` endpoint. The code includes setting search parameters like categories, location, filters, and limit, and then processes the response, checking for a success status code (20000).

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task business_data_business_listings_search_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                //DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))

            };

            var postData = new List<object>();

            // You can set only one task at a time

            postData.Add(new

            {

                categories = new[]

                {

                    "pizza_restaurant"

                },

                description = "pizza",

                title = "pizza",

                is_claimed = true,

                location_coordinate = "53.476225,-2.243572,10",

                order_by = new[]

                {

                    "rating.value,desc"

                },

                filters = new object[]

                {

                    new object[] { "rating.value", ">", 3 }

                },

                limit = 3

            });

            // POST /v3/business_data/business_listings/search/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/business_data/business_listings/search/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Post Lighthouse Task via Bash

Source: https://docs.dataforseo.com/v3/on_page/lighthouse/task_post

This Bash script demonstrates how to send a POST request to the Dataforseo API to initiate an on-page Lighthouse task. It includes authentication using a Base64 encoded login and password, and specifies task details like URL, mobile optimization preference, and pingback URL.

```bash
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access 

login="login" 

password="password" 

cred="$(printf ${login}:${password} | base64)" 

curl --location --request POST "https://api.dataforseo.com/v3/on_page/lighthouse/task_post" 

--header "Authorization: Basic ${cred}"  

--header "Content-Type: application/json" 

--data-raw "[

  {

    "url": "https://dataforseo.com",

    "for_mobile": true,

    "tag": "some_string_123",

    "pingback_url": "https://your-server.com/pingscript?id=$id&tag=$tag"

  }

]"
```

--------------------------------

### Get Amazon Locations List (Node.js)

Source: https://docs.dataforseo.com/v3/merchant/amazon/locations

Fetches Amazon locations using Node.js with the Axios HTTP client. This example demonstrates making a GET request to the API, including authentication, and specifying a country filter. The response data, specifically the 'result' array, is logged to the console.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/merchant/amazon/locations',

    auth: {

        username: 'login',

        password: 'password'

    },

    data: [{

        country: "us"

    }],

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get Ad Traffic By Keywords Task Result using Node.js

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/ad_traffic_by_keywords/task_get_php=

This Node.js example uses the axios library to make a GET request to the DataForSEO API for ad traffic by keywords data. It demonstrates how to include authentication credentials and content type headers in the request. The response data, containing the task results, is logged to the console.

```javascript
const task_id = '02231934-2604-0066-2000-570459f04879';



const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/keywords_data/google_ads/ad_traffic_by_keywords/task_get/' + task_id,

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get Google Ads Keywords Data via Python

Source: https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/live_php=

This Python example uses the RestClient class to interact with the DataforSEO API. It demonstrates how to initialize the client with API credentials, prepare the POST data containing location and target information, and send the request to retrieve keyword data.

```python
from client import RestClient
# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("login", "password")
post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    location_name="United States",
    target="dataforseo.com"
)
# POST /v3/keywords_data/google_ads/keywords_for_site/live
# the full list of possible parameters is available in documentation
response = client.post("/v3/keywords_data/google_ads/keywords_for_site/live", post_data)
```

--------------------------------

### Fetch Google SERP Competitors Live Data

Source: https://docs.dataforseo.com/v3/dataforseo_labs/google/serp_competitors/live_php=

Demonstrates how to use the DataForSEO API to get live Google SERP competitor data. It includes setting up an HTTP client with authentication, constructing the POST request body with keywords, location, language, and filters, sending the request, and deserializing the JSON response. Error handling for the API call is also included. Requires Newtonsoft.Json and System.Net.Http libraries.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task dataforseo_labs_google_serp_competitors_live()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            postData.Add(new

            {

                keywords = new[]

                {

                    "phone",

                    "watch"

                },

                location_name = "United States",

                language_name = "English",

                filters = new object[]

                {

                    new object[] { "relevant_serp_items", ">", 0 },

                    "or",

                    new object[] { "median_position", "in", new object[] { 1, 10 } }

                }

            });

            // POST /v3/dataforseo_labs/google/serp_competitors/live

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/dataforseo_labs/google/serp_competitors/live", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Google Ad Traffic by Keywords Task Results (JavaScript/Node.js)

Source: https://docs.dataforseo.com/v3/keywords_data/google/ad_traffic_by_keywords/task_get

This Node.js example uses the axios library to make a GET request to the DataForSEO API for Google Ad Traffic by Keywords. It demonstrates how to authenticate using basic auth and specify the endpoint for retrieving task results by ID. The response data is logged to the console.

```javascript
const task_id = '02231934-2604-0066-2000-570459f04879';



const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/keywords_data/google/ad_traffic_by_keywords/task_get/' + task_id,

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Pingback URL Example

Source: https://docs.dataforseo.com/v2/rnk_csharp=

This example illustrates how to configure a `pingback_url` to receive notifications when a task is completed. The `$task_id` and `$post_id` variables are placeholders that the API will populate with the relevant task and post IDs.

```string
http://your-server.com/pingscript?taskId=$task_id&postId=$post_id
```

--------------------------------

### Get Keyword ID using C#

Source: https://docs.dataforseo.com/v2/cmn

Demonstrates how to fetch a keyword ID using C# and HttpClient. This example sets up the HTTP client with base address and authorization headers. It's part of the DataForSeoDemos namespace and requires appropriate .NET libraries.

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
namespace DataForSeoDemos
{
    public static partial class Demos
    {
        public static async Task cmn_key_id()
        {
            var httpClient = new HttpClient
            {
                BaseAddress = new Uri("https://api.dataforseo.com/"),
                //Instead of 'login' and 'password' use your credentials from https://my.dataforseo.com/#api_dashboard
                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password")))
            }
        };

```

--------------------------------

### Make SERP Live HTML Request (C#)

Source: https://docs.dataforseo.com/v3/serp/google/finance_explore/live/html

This C# code example shows how to make a live HTML request to the Google Finance Explore API using DataForSEO. It includes setting up an HttpClient, defining request parameters, sending a POST request, and deserializing the JSON response. Error handling is included to display status codes and messages.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_live_html()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                //DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            // You can set only one task at a time

            postData.Add(new

            {

                language_code = "en",

                location_code = 2840

            });

            // POST /v3/serp/google/finance_explore/live/html

            // in addition to 'google' and 'finance_explore' you can also set other search engine and type parameters

            // the full list of possible parameters is available in documentation

            var taskPostResponse = await httpClient.PostAsync("/v3/serp/google/finance_explore/live/html", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject<dynamic>(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Merchant Amazon Sellers Tasks Ready (PHP)

Source: https://docs.dataforseo.com/v3/merchant/amazon/sellers/tasks_ready

This PHP example utilizes a RestClient to interact with the Dataforseo API. It shows how to initialize the client with credentials and retrieve a list of completed tasks for Amazon sellers. Error handling for API requests is also included.

```php
<?php

require('RestClient.php');

$api_url = 'https://api.dataforseo.com/';

// Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

$client = new RestClient($api_url, null, 'login', 'password');



try {

   // using this method you can get a list of completed tasks

   // GET /v3/merchant/amazon/sellers/tasks_ready

   $result = $client->get('/v3/merchant/amazon/sellers/tasks_ready');

   print_r($result);

   // do something with result

} catch (RestClientException $e) {

   echo "n";

   print "HTTP code: {$e->getHttpCode()}n";

   print "Error code: {$e->getCode()}n";

   print "Message: {$e->getMessage()}n";

   print  $e->getTraceAsString();

   echo "n";

}

$client = null;

?>
```

--------------------------------

### Fetch Apple Locations using Node.js Axios

Source: https://docs.dataforseo.com/v3/app_data/apple/locations

This JavaScript example utilizes the Axios library to make a GET request to the DataForSEO API for Apple app locations. It demonstrates how to set up authentication using the `auth` object and include necessary headers. The result data is logged to the console, and errors are caught and logged.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/app_data/apple/locations',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```

--------------------------------

### Get Google Business Locations via DataForSEO API (C#)

Source: https://docs.dataforseo.com/v3/business_data/google/locations

This C# example demonstrates how to asynchronously fetch Google business locations using HttpClient. It includes setting up authentication headers, making the GET request, and deserializing the JSON response, along with error checking.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task business_data_locations()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of locations

            // GET /v3/business_data/google/locations/$country

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/business_data/google/locations/gb");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### C#: Fetch DataForSEO Serp Locations API

Source: https://docs.dataforseo.com/v3/serp/seznam/locations

This C# example demonstrates how to fetch a list of locations using the DataForSEO SERP API. It includes setting up an HttpClient with authentication, making a GET request to the '/v3/serp/seznam/locations' endpoint, and deserializing the JSON response. Error handling based on status code is also included.

```csharp
using Newtonsoft.Json;

using System;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task serp_locations()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            // using this method you can get a list of locations

            // GET /v3/serp/seznam/locations

            // in addition to 'seznam' you can also set other search engine

            // the full list of possible parameters is available in documentation

            var response = await httpClient.GetAsync("/v3/serp/seznam/locations");

            var result = JsonConvert.DeserializeObject(await response.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Post Google My Business Info Task (C#)

Source: https://docs.dataforseo.com/v3/business_data/google/my_business_info/task_post

This C# example demonstrates how to post tasks to the DataForSEO Google My Business Info API using an HttpClient. It includes setting up authentication, defining task parameters (with and without optional fields like priority and pingback URL), and handling the API response. The 'Newtonsoft.Json' library is used for JSON serialization and deserialization.

```csharp
using Newtonsoft.Json;

using System;

using System.Collections.Generic;

using System.Net.Http;

using System.Net.Http.Headers;

using System.Text;

using System.Threading.Tasks;



namespace DataForSeoDemos

{

    public static partial class Demos

    {

        public static async Task business_data_info_task_post()

        {

            var httpClient = new HttpClient

            {

                BaseAddress = new Uri("https://api.dataforseo.com/"),

                // Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access

                DefaultRequestHeaders = { Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(Encoding.ASCII.GetBytes("login:password"))) }

            };

            var postData = new List<object>();

            // example #1 - a simple way to set a task

            // this way requires you to specify a location, a language of search, and a keyword.

            postData.Add(new

            {

                language_code = "en",

                location_code = 1023191,

                keyword = "RustyBrick, Inc."

            });

            // example #2 - a way to set a task with additional parameters

            // high priority allows us to complete a task faster, but you will be charged more credits.

            // after a task is completed, we will send a GET request to the address you specify. Instead of $id and $tag, you will receive actual values that are relevant to this task.

            postData.Add(new

            {

                language_name = "English",

                location_name = "New York,New York,United States",

                keyword = "RustyBrick, Inc.",

                priority = 2,

                tag = "some_string_123",

                pingback_url = "https://your-server.com/pingscript?id=$id&tag=$tag"

            });

            // POST /v3/business_data/google/my_business_info/task_post

            var taskPostResponse = await httpClient.PostAsync("/v3/business_data/google/my_business_info/task_post", new StringContent(JsonConvert.SerializeObject(postData)));

            var result = JsonConvert.DeserializeObject(await taskPostResponse.Content.ReadAsStringAsync());

            // you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors

            if (result.status_code == 20000)

            {

                // do something with result

                Console.WriteLine(result);

            }

            else

                Console.WriteLine($"error. Code: {result.status_code} Message: {result.status_message}");

        }

    }

}

```

--------------------------------

### Get Merchant Google Products Tasks Ready (Bash)

Source: https://docs.dataforseo.com/v3/merchant/google/products/tasks_ready_php=

This Bash script demonstrates how to make a GET request to the DataForSEO API to retrieve a list of completed tasks for Google product data. It includes authentication using a base64 encoded string of login and password.

```bash
# Instead of 'login' and 'password' use your credentials from https://app.dataforseo.com/api-access 

login="login" 

password="password"

cred="$(printf ${login}:${password} | base64)"

curl --location --request GET "https://api.dataforseo.com/v3/merchant/google/products/tasks_ready" 

--header "Authorization: Basic ${cred}"  

--header "Content-Type: application/json" 

--data-raw ""
```

--------------------------------

### Fetch Google Organic Tasks (Node.js)

Source: https://docs.dataforseo.com/v3/serp/google/organic/tasks_fixed

This Node.js example uses the `axios` library to perform a GET request to the DataForSEO API. It demonstrates how to set up authentication using basic auth with username and password, specify headers, and handle the response or errors. The 'result' field from the API response is logged to the console.

```javascript
const axios = require('axios');



axios({

    method: 'get',

    url: 'https://api.dataforseo.com/v3/serp/google/organic/tasks_fixed',

    auth: {

        username: 'login',

        password: 'password'

    },

    headers: {

        'content-type': 'application/json'

    }

}).then(function (response) {

    var result = response['data']['tasks'][0]['result'];

    // Result data

    console.log(result);

}).catch(function (error) {

    console.log(error);

});
```
