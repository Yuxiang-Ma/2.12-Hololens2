using Microsoft.MixedReality.Toolkit;
using System;
using System.Collections;
using System.IO;
using System.Net;
using TMPro;
using UnityEngine;
using System.Buffers;
using UnityEngine.Rendering;

public class PngShow : MonoBehaviour
{
    public MeshRenderer frame;    //Mesh for displaying video

    public static string ServerIp = "10.29.9.107";

    //public static string MobileURL = $"10.29.9.107:4000/uploads/display_image.png";
    //public static string MobileURL = "10.29.81.150:2000/video";
    public static string MobileURL = "https://thumbs.dreamstime.com/b/jpg-spelled-word-dice-letters-reflection-term-toy-cubes-bottom-studio-shot-white-background-46803015.jpg";
    public static string UR5URL = "muffin.local:8080/?action=stream";

    private string sourceURL;

    private Texture2D texture;
    private Stream stream;
    public TextMeshPro textMesh;

    //private string boundary = "--boundarydonotcross";
    //private TouchScreenKeyboard _urlKeyboard;

    private State _state;
    void Start()
    {
        _state = State.Mobile;
        sourceURL = FormatURL(_state == State.Mobile ? MobileURL : UR5URL);
        if (textMesh != null)
        {
            textMesh.text = $"stream is starting\n";
            textMesh.text += $"stream:{sourceURL}\n";
            textMesh.text += $"video display:{_state}";
        }
        texture = new Texture2D(2, 2);
        Debug.Log($"test: {sourceURL}");
        StartStream();
    }

    public void OnSwtichVideoButtonClicked()
    {
        _state = _state == State.Mobile ? State.UR5 : State.Mobile;
        // restart stream after swtich
        StartStream();
    }

    public void OnEditSourceUrlButtonClicked()
    {
        var keyboardInputManager = FindObjectOfType<KeyboardInputManager>();
        keyboardInputManager.RequestKeyboardInput(KeyboardInputManager.InputMode.MobileRobotVideoIPAddress, newUrl =>
        {
            UpdateURL(newUrl);
            if (sourceURL != newUrl)
            {
                sourceURL = FormatURL(newUrl);
                StartStream();
            }
        });
    }

    private void UpdateURL(string newUrl)
    {
        if (_state == State.Mobile)
        {
            if (FormatURL(MobileURL) != newUrl)
            {
                MobileURL = newUrl;
                StartStream();
            }
        }
        else
        {
            if (FormatURL(UR5URL) != newUrl)
            {
                UR5URL = newUrl;
                StartStream();
            }
        }
    }


    private void StartStream()
    {
        if (stream != null)
        {
            stream.Close();
        }
        try
        {
            // always update source URL before start Stream
            sourceURL = FormatURL(_state == State.Mobile ? MobileURL : UR5URL);
            // create HTTP request
            HttpWebRequest req = (HttpWebRequest)WebRequest.Create(sourceURL);
            //Optional (if authorization is Digest)
            req.Credentials = new NetworkCredential("username", "password");
            // get response
            WebResponse resp = req.GetResponse();
            // get response stream
            stream = resp.GetResponseStream();
        }
        catch (WebException e)
        {
            Debug.Log("Error: " + e.Status);
            textMesh.text = $"Invalid IP address{sourceURL}\n";
            textMesh.text += $"video display:{_state}";
            return;
        }
        //GetFrame();
        StartCoroutine(GetFrame());

    }

    IEnumerator GetFrame()
    {
        byte[] JpegData = new byte[640 * 480];
        Debug.Log("JpegData initialized...");

        while (true)
        {
            int bytesToRead = FindLength(stream);
            //int bytesToRead = JpegData.Length;
            Debug.Log($"bytesToRead: {bytesToRead}");
            if (stream.ReadByte() == -1)
            {
                print("No stream read");
                yield break;
            }

            if (bytesToRead < 0)
                bytesToRead = JpegData.Length;

            int leftToRead = bytesToRead;

            while (leftToRead > 0)
            {
                leftToRead -= stream.Read(JpegData, bytesToRead - leftToRead, leftToRead);
                //Debug.Log($"Data Left to Read: {leftToRead}");
                yield return null;
            }

            if (textMesh != null)
            {
                var floatingText = $"stream is read {bytesToRead}\n";
                floatingText += $"Video URL: {sourceURL}\n";
                floatingText += $"video display:{_state}";
                textMesh.text = floatingText;
            }

            texture.LoadImage(JpegData);
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
    private static string FormatURL(string inputURL) // adds http:// to beginning of URL for quicker changing of URL in HoloLens.
    {
        return $"http://{inputURL}";
    }

    private enum State
    {
        UR5,
        Mobile,
    }
}

