using System;
using System.Collections;
using System.IO;
using System.Net;
using TMPro;
using UnityEngine;
using UnityEngine.Video;

public class WebStream : MonoBehaviour
{
    public MeshRenderer frame;    //Mesh for displaying video

    public string sourceURL = "10.189.3.42:3000";
    sourceURL = "http://" + sourceURL + "/stream"; // makes it easier to change the URL in the inspector
    private Texture2D texture;
    private Stream stream;
    private VideoPlayer videoPlayer;
    public TextMeshPro textMesh = null;

    private TouchScreenKeyboard _urlKeyboard;

    void Start()
    {
        if (textMesh == null)
        {
            textMesh = GetComponent<TextMeshPro>();
            textMesh.text = $"stream is starting";
        }

        texture = new Texture2D(2, 2);
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
        var keyboardInputManager = FindObjectOfType<KeyboardInputManager>();
        keyboardInputManager.RequestKeyboardInput(KeyboardInputManager.InputMode.URL, newUrl =>
        {
            if (sourceURL != newUrl)
            {
                sourceURL = newUrl;
                sourceURL = "http://" + sourceURL + "/stream"; // makes it easier to change the URL in the inspector
                StartStream();
            }
        });
    }


    private void StartStream()
    {
        if (videoPlayer != null)
        {
            videoPlayer.Stop();
        }

        videoPlayer = gameObject.AddComponent<VideoPlayer>();
        videoPlayer.url = sourceURL;
        videoPlayer.isLooping = true;
        videoPlayer.renderMode = VideoRenderMode.MaterialOverride;
        videoPlayer.targetMaterialRenderer = frame;
        videoPlayer.targetMaterialProperty = "_MainTex";
        videoPlayer.Play();
    }

    // IEnumerator GetFrame()
    // {
    //     Byte[] JpegData = new Byte[640*480];

    //     while (true)
    //     {
    //         int bytesToRead = FindLength(stream);
    //         if (textMesh == null)
    //         {
    //             textMesh = GetComponent<TextMeshPro>();
    //             textMesh.text = $"stream is read {bytesToRead}";
    //         }
    //         print(bytesToRead);
    //         if (bytesToRead == -1)
    //         {
    //             print("End of stream");
    //             yield break;
    //         }

    //         int leftToRead = bytesToRead;

    //         while (leftToRead > 0)
    //         {
    //             leftToRead -= stream.Read(JpegData, bytesToRead - leftToRead, leftToRead);
    //             yield return null;
    //         }

    //         MemoryStream ms = new MemoryStream(JpegData, 0, bytesToRead, false, true);

    //         texture.LoadImage(ms.GetBuffer());
    //         frame.material.mainTexture = texture;
    //         stream.ReadByte(); // CR after bytes
    //         stream.ReadByte(); // LF after bytes
    //     }
    // }


    // int FindLength(Stream stream)
    // {
    //     int b;
    //     string line = "";
    //     int result = -1;
    //     bool atEOL = false;

    //     while ((b = stream.ReadByte()) != -1)
    //     {
    //         if (b == 10) continue; // ignore LF char
    //         if (b == 13)
    //         { // CR
    //             if (atEOL)
    //             {  // two blank lines means end of header
    //                 stream.ReadByte(); // eat last LF
    //                 return result;
    //             }
    //             if (line.StartsWith("Content-Length:"))
    //             {
    //                 result = Convert.ToInt32(line.Substring("Content-Length:".Length).Trim());
    //             }
    //             else
    //             {
    //                 line = "";
    //             }
    //             atEOL = true;
    //         }
    //         else
    //         {
    //             atEOL = false;
    //             line += (char)b;
    //         }
    //     }
    //     return -1;
    // }
}
