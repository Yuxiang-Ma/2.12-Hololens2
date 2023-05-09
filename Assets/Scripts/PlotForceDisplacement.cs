using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Net;

public class LoadIMG : MonoBehaviour
{
    public GameObject MyImage;
    public WWW www;
    public string ServerIp;
    private bool _ipChanged;


    void Start()
    {
        UpdateImage();
    }


    void Update()
    {
        UpdateImage();
    }

    public void OnEditHostIpButtonClicked()
    {
        var keyboardInputManager = FindObjectOfType<KeyboardInputManager>();
        keyboardInputManager.RequestKeyboardInput(KeyboardInputManager.InputMode.ServerIPAddress, newInput =>
        {
            if (ServerIp != newInput)
            {
                ServerIp = newInput;
                _ipChanged = true;
            }
        });
    }


    void UpdateImage()
    {
        try
        {
            WebClient client = new WebClient();
            byte[] myDataBuffer = client.DownloadData("http://192.168.0.3:4000/uploads/display_image.png");

            Texture2D tex = new Texture2D(2, 2); // Create an empty Texture; size doesn't matter (she said)
            tex.LoadImage(myDataBuffer);

            MyImage = GameObject.Find("RawImage");
            MyImage.GetComponent<RawImage>().texture = tex;
        }
        catch
        {
            print("Failed to load image.");
        }
    }
}