package com.example.edgeclientsample

import android.os.Bundle
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.Response
import com.android.volley.toolbox.BasicNetwork
import com.android.volley.toolbox.HurlStack
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.snackbar.Snackbar
import kotlinx.coroutines.*

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {

        print("Creating activity")
        Log.d("Request", "Creating activity")

        val ip : String = intent.getStringExtra("server_ip").toString()
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(findViewById(R.id.toolbar))

        // Instantiate the RequestQueue.
        val queue = Volley.newRequestQueue(this)

        //val url = BuildConfig.MEC_HOST_URL
        val default_url = "http://192.168.1.57:8080"
        Log.d("Request", "Is ip: ${ip}")
        Log.d("Request", "Is ip null? ${ip.compareTo("null")}")

        val url = if (ip.compareTo("null") != 0) ip else default_url
            //ip ?: default_url //BuildConfig.MEC_HOST_URL

        GlobalScope.launch {
            makeRequest(queue, url, 2000, 10)
        }
    }

    /*This function receives a RequestQueue queue, an interval between
    packets interPacketTime, and the number of requests nRequests. It sends
    to the edge server nRequests, with an interval of interPacketTime between them.
     */
    private suspend fun makeRequest(queue : RequestQueue,
                                    url : String,
                                    interPacketTime : Long,
                                    nRequests : Int) {


        return withContext(Dispatchers.IO) {
            for (i in 1..nRequests) {
                delay(interPacketTime)
                // Request a string response from the provided URL.
                print("Requesting ${url} ")
                Log.d("Request", "Requesting ${url} ")
                val stringRequest = StringRequest(
                        Request.Method.GET, url,
                        Response.Listener<String> { response ->
                            println("Response is: ${response}")
                            Log.d("Request", "Response is: ${response}")
                        },
                        Response.ErrorListener { error ->
                            println(error.toString())
                        })
                // Add the request to the RequestQueue.
                queue.add(stringRequest)

            }
        }
    }
}