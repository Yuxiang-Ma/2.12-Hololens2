using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class LoadDisplay1 : MonoBehaviour
{
    GameObject image;
    string filename = "./img/ur5_force.png";

    void Start()
    {
        var rawData = System.IO.File.ReadAllBytes(filename);
        Texture2D tex = new Texture2D(2, 2); // Create an empty Texture; size doesn't matter (she said)
        tex.LoadImage(rawData);

        image = GameObject.Find("Display1");
        image.GetComponent<RawImage>().texture = tex;
    }

    void Update()
    {
        Texture2D tex = new Texture2D(2, 2); // Create an empty Texture; size doesn't matter (she said)

        try
        {
            var rawData = System.IO.File.ReadAllBytes(filename);
            tex.LoadImage(rawData);
            image.GetComponent<RawImage>().texture = tex;
        }
        catch{}
    }
}