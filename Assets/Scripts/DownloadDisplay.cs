using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Net;

public class DownloadDisplay : MonoBehaviour
{
    public GameObject MyImage;
    public WWW www;
    public string ForceDisplacementIP;

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
        keyboardInputManager.RequestKeyboardInput(KeyboardInputManager.InputMode.ForceDisplacementImageFeedIPAddress, newInput =>
        {
            if (ForceDisplacementIP != newInput)
            {
                ForceDisplacementIP = newInput;
                _ipChanged = true;
            }
        });
    }

    void UpdateImage()
    {
        try
        {
            WebClient client = new WebClient();
            string serverIp = RobotController.ServerIp;
            byte[] myDataBuffer = client.DownloadData($"http://{ForceDisplacementIP}:4000/uploads/display_image.png");

            Texture2D tex = new Texture2D(2, 2);
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
