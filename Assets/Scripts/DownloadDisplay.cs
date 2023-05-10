using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class DownloadDisplay : MonoBehaviour
{
    string serverIp = RobotController.ServerIp; // Set this in the inspector
    private RawImage myRawImage;
    private Texture2D tex;

    void Start()
    {
        GameObject myImage = GameObject.Find("RawImage");
        myRawImage = myImage.GetComponent<RawImage>();
        tex = new Texture2D(2, 2);
        UpdateImage();
    }

    void UpdateImage()
    {
        StartCoroutine(DownloadImage());
    }

    IEnumerator DownloadImage()
    {
        using (UnityWebRequest www = UnityWebRequestTexture.GetTexture($"http://{serverIp}:4000/uploads/display_image.png"))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                tex = ((DownloadHandlerTexture)www.downloadHandler).texture;
                myRawImage.texture = tex;
            }
        }
    }
}
