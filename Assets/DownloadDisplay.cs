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

    void Start()
    {
        UpdateImage();
    }


    void Update()
    {
        UpdateImage();
    }

    void UpdateImage()
    {
        try
        {
            WebClient client = new WebClient();
            byte[] myDataBuffer = client.DownloadData("http://192.168.0.3:4000/uploads/display_image.png");

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
