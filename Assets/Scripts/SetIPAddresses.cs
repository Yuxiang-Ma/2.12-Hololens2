using UnityEngine;

public class IPManager : MonoBehaviour
{
    public static string ServerIP = "10.29.14.59";
    public static string MobileRobotVideoIP = "10.11.11.11";
    public static string ForceDisplacementImageFeedIP = "10.29.11.11";
    public static string UR5RealSenseIP = "10.28.14.14";

    private bool _ipChanged = false;

    public void OnServerIPButtonClicked()
    {
        var keyboardInputManager = FindObjectOfType<KeyboardInputManager>();
        keyboardInputManager.RequestKeyboardInput(KeyboardInputManager.InputMode.ServerIPAddress, newInput =>
        {
            if (ServerIP != newInput)
            {
                ServerIP = newInput;
                _ipChanged = true;
            }
        });
    }

    public void OnMobileRobotVideoIPButtonClicked()
    {
        var keyboardInputManager = FindObjectOfType<KeyboardInputManager>();
        keyboardInputManager.RequestKeyboardInput(KeyboardInputManager.InputMode.MobileRobotVideoIPAddress, newInput =>
        {
            if (MobileRobotVideoIP != newInput)
            {
                MobileRobotVideoIP = newInput;
                _ipChanged = true;
            }
        });
    }

    public void OnForceDisplacementImageFeedIPButtonClicked()
    {
        var keyboardInputManager = FindObjectOfType<KeyboardInputManager>();
        keyboardInputManager.RequestKeyboardInput(KeyboardInputManager.InputMode.ForceDisplacementImageFeedIPAddress, newInput =>
        {
            if (ForceDisplacementImageFeedIP != newInput)
            {
                ForceDisplacementImageFeedIP = newInput;
                _ipChanged = true;
            }
        });
    }

    public void OnUR5RealSenseIPButtonClicked()
    {
        var keyboardInputManager = FindObjectOfType<KeyboardInputManager>();
        keyboardInputManager.RequestKeyboardInput(KeyboardInputManager.InputMode.UR5RealSenseIPAddress, newInput =>
        {
            if (UR5RealSenseIP != newInput)
            {
                UR5RealSenseIP = newInput;
                _ipChanged = true;
            }
        });
    }

    private void Update()
    {
        if (_ipChanged)
        {
            // Add your code to handle the IP change here
            _ipChanged = false;
        }
    }
}
