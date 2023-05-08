using UnityEngine;

public class KeyboardInputManager : MonoBehaviour
{
    public enum InputMode
    {
        None,
        IPAddress,
        URL
    }

    private InputMode currentInputMode = InputMode.None;
    private TouchScreenKeyboard keyboard;
    private System.Action<string> currentCallback;

    public void RequestKeyboardInput(InputMode mode, System.Action<string> callback)
    {
        currentInputMode = mode;
        currentCallback = callback;
        switch (mode)
        {
            case InputMode.IPAddress:
                keyboard = TouchScreenKeyboard.Open("", TouchScreenKeyboardType.DecimalPad, false, false, false);
                break;
            case InputMode.URL:
                keyboard = TouchScreenKeyboard.Open("", TouchScreenKeyboardType.URL, false, false, false);
                break;
        }
    }

    void Update()
    {
        if (currentInputMode == InputMode.None) return;

        if (keyboard != null && (keyboard.status == TouchScreenKeyboard.Status.Done || keyboard.status == TouchScreenKeyboard.Status.Canceled))
        {
            currentCallback?.Invoke(keyboard.text);
            currentInputMode = InputMode.None;
            keyboard = null;
        }
    }
}
