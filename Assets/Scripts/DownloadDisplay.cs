using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Net;
using System.Threading;
using UnityEditor.PackageManager;

public class DownloadDisplay : MonoBehaviour
{
    public GameObject MyImage;
    public WWW www;
    WebClient client = new WebClient();

    void Start()
    {
        UpdateImage();
    }


    void Update()
    {
        //client.Proxy = null;
        //UpdateImage();
        //Thread.Sleep(1000   );
    }

    void UpdateImage()
    {
        try
        {
            
            string serverIp = RobotController.ServerIp;
            byte[] myDataBuffer = client.DownloadData($"http://{serverIp}:4000/uploads/display_image.png");
            //byte[] myDataBuffer = client.DownloadData($"https://creazilla-store.fra1.digitaloceanspaces.com/icons/3220140/tick-small-icon-md.png");
        
            //Texture2D tex = new Texture2D(2, 2);
            //tex.LoadImage(myDataBuffer);

            //MyImage = GameObject.Find("RawImage");
            //MyImage.GetComponent<RawImage>().texture = tex;
        }
        catch
        {
            print("Failed to load image.");
        }
    }
}
