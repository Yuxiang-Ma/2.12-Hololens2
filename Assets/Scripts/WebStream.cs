using System;
using System.Collections;
using System.IO;
using System.Net;
using TMPro;
using UnityEngine;

public class WebStream : MonoBehaviour
{
    public MeshRenderer frame;    //Mesh for displaying video

    public static string IpURL = "10.29.17.61:3000";

    public static string FormatURL(string inputURL, string portValue) // adds http:// to beginning of URL for quicker changing of URL in HoloLens.
    {
        return $"http://{inputURL}:{portValue}";
    }

    public string sourceURL = FormatURL(IpURL);

    private Texture2D texture;
    private Stream stream;
    public TextMeshPro textMesh = null;

    private TouchScreenKeyboard _urlKeyboard;

    void Start()
    {
        ipAddresses = new List<string>()
            {
                IPManager.MobileRobotVideoIP,
                IPManager.UR5RealSenseIP
            };
            
        if (textMesh == null)
        {
            textMesh = GetComponent<TextMeshPro>();
            textMesh.text = $"stream is starting";
        }
        texture = new Texture2D(2, 2);
        Debug.Log($"test: {sourceURL}");
        StartStream();
    }

    // void Update()
    // {
    //     if (_urlKeyboard?.status == TouchScreenKeyboard.Status.Done
    //         || _urlKeyboard?.status == TouchScreenKeyboard.Status.Canceled)
    //     {
    //         if (sourceURL != _urlKeyboard.text)
    //         {
    //             sourceURL = _urlKeyboard.text;
    //             StartStream();
    //         }
    //         _urlKeyboard = null;
    //     }
    // }

    public void OnEditSourceUrlButtonClicked()
    {
        // Cycle through the list of IP addresses
        currentIpIndex = (currentIpIndex + 1) % ipAddresses.Count;

        var newUrl = ipAddresses[currentIpIndex];
        string portValue = "";

        if (newUrl == IPManager.MobileRobotVideoIP)
        {
            _portValue = "3000";
        }
        else if (newUrl == IPManager.UR5RealSenseIP)
        {
            _portValue = "5000";
        }

        if (sourceURL != newUrl)
        {
            sourceURL = FormatURL(newUrl,_portValue);
            StartStream();
        }
    }


    private void StartStream()
    {
        if (stream != null)
        {
            stream.Close();
        }

        // create HTTP request
        
        HttpWebRequest req = (HttpWebRequest)WebRequest.Create(sourceURL);
        //Optional (if authorization is Digest)
        req.Credentials = new NetworkCredential("username", "password");
        // get response
        WebResponse resp = req.GetResponse();
        // get response stream
        stream = resp.GetResponseStream();
        StartCoroutine(GetFrame());
    }

    IEnumerator GetFrame()
    {
        Byte[] JpegData = new Byte[640*480];

        Debug.Log("JpegData initialized...");

        while (true)
        {
            int bytesToRead = FindLength(stream);
            if (textMesh == null)
            {
                textMesh = GetComponent<TextMeshPro>();
                var floatingText = $"stream is read {bytesToRead}\n";
                floatingText += $"Video URL: {sourceURL}";
                textMesh.text = floatingText;
            }
            Debug.Log("TextMesh Updated...");
            print(bytesToRead);
            if (bytesToRead == -1)
            {
                print("End of stream");
                yield break;
            }

            int leftToRead = bytesToRead;

            while (leftToRead > 0)
            {
                leftToRead -= stream.Read(JpegData, bytesToRead - leftToRead, leftToRead);
                Debug.Log($"Data Left to Read: {leftToRead}");
                yield return null;
            }

            MemoryStream ms = new MemoryStream(JpegData, 0, bytesToRead, false, true);

            texture.LoadImage(ms.GetBuffer());
            frame.material.mainTexture = texture;
            stream.ReadByte(); // CR after bytes
            stream.ReadByte(); // LF after bytes
        }
    }


    int FindLength(Stream stream)
    {
        int b;
        string line = "";
        int result = -1;
        bool atEOL = false;

        while ((b = stream.ReadByte()) != -1)
        {
            if (b == 10) continue; // ignore LF char
            if (b == 13)
            { // CR
                if (atEOL)
                {  // two blank lines means end of header
                    stream.ReadByte(); // eat last LF
                    return result;
                }
                if (line.StartsWith("Content-Length:"))
                {
                    result = Convert.ToInt32(line.Substring("Content-Length:".Length).Trim());
                }
                else
                {
                    line = "";
                }
                atEOL = true;
            }
            else
            {
                atEOL = false;
                line += (char)b;
            }
        }
        return -1;
    }
}
