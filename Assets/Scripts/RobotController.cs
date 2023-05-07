using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;
using TMPro;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Linq;
using Microsoft.MixedReality.Toolkit.UI;

/**
 * This module is an example of how to communicate with the UR5 robot via a relay.
 * It constantly fetches joint torques from UR5 and displays it.
 *
 * Author: Chengyuan Ma.
 */
public class RobotController : MonoBehaviour
{
    // Edit relay IP from the Unity Editor.
    public string ServerIp;
    public int Port = 21200;
    public int TimeoutMs = 2000;
    public TextMeshPro TextMesh;

    // slider control for chest compression
    public float Amp = 60;      // mm
    public float Freq =  110;      // freq

    public TouchSliderValue AmplitudeSlider;
    public TouchSliderValue FrequencySlider;
    // We do all the networking in a dedicated thread / task.
    // The networking thread writes the received data while the main thread reads them.
    // We need a lock to prevent data 
    private object _lock = new();

    private State _state;

    private bool _stateChanged;

    private bool _sliderChanged;

    private bool _connected;

    // These fields may help changing the relay IP through a virtual keyboard while 
    // the app is running, but it has not been thoroughly tested xD.
    private bool _ipChanged;
    private TouchScreenKeyboard _keyboard;

    private float[] _jointTorques;

    // Start is called before the first frame update
    void Start()
    {
        _connected = false;
        _ipChanged = false;
        _jointTorques = new float[6];
        _state = State.ArmUp;
        _stateChanged = false;
        _sliderChanged = false;
        Task.Run(ConnectionLoop);
    }

    // Update is called once per frame
    void Update()
    {
        // if (_keyboard?.status == TouchScreenKeyboard.Status.Done
        //     || _keyboard?.status == TouchScreenKeyboard.Status.Canceled)
        // {
        //     if (ServerIp != _keyboard.text)
        //     {
        //         ServerIp = _keyboard.text;
        //         _ipChanged = true;
        //     }
        //     _keyboard = null;
        // }

        var text = "2.12 Starter App\n";
        var serverIp = _keyboard == null ? ServerIp : _keyboard.text;
        var status = _connected ? "Connected" : "Disconnected";
        text += $"Server IP: {serverIp} ({status})\n";
        text += "Torques: " + string.Join(", ", _jointTorques.Select(torque => $"{torque:00.00}")) + "\n";
        text += "Arm currently " + (_state == State.ArmUp ? "UP" : "DOWN"+"\n");
        text += $"CPR amplitude {Amp:N}mm, frequency {Freq:N} cpm";
        TextMesh.text = text;
    }

    // The networking thread.
    void ConnectionLoop()
    {
        while (true)
        {
            Socket socket = null;
            try
            {
                _connected = false;
                socket = new Socket(SocketType.Stream, ProtocolType.Tcp);
                socket.SendTimeout = TimeoutMs;
                socket.ReceiveTimeout = TimeoutMs;
                socket.Connect(ServerIp, Port);
                _connected = true;
                _ipChanged = false;

                var buffer = new byte[1024];
                while (true)
                {
                    if (_ipChanged)
                    {
                        try { socket.Close(); } catch { }
                        break;
                    }

                    var message = " ";
                    if (_stateChanged)
                    {
                        message = "Arm state changed\n";
                        message = _state == State.ArmUp ? "UP" : "DOWN";
                        _stateChanged = false;
                    }
                    socket.Send(Encoding.UTF8.GetBytes(message));

                    if (_sliderChanged)
                    {
                        message = "Slider value changed\n";
                        message += $"Amp:{Amp:N}\n";
                        message += $"Freq:{Freq:N}\n";
                        _sliderChanged = false;
                    }
                    socket.Send(Encoding.UTF8.GetBytes(message));
                    var count = socket.Receive(buffer);
                    // The server replies with 24 bytes, representing 6 floats in network 
                    // byte order (big endian).
                    const int floatWidth = 4;

                    // Ensures that `buffer` holds the floats in native endianness.
                    if (BitConverter.IsLittleEndian)
                        for (var i = 0; i < count; i += floatWidth)
                            Array.Reverse(buffer, i, floatWidth);

                    lock (_lock)
                    {
                        Debug.Assert(count / floatWidth == _jointTorques.Length);
                        // Update the _jointTorques array.
                        for (var i = 0; i < _jointTorques.Length; i++)
                            _jointTorques[i] = BitConverter.ToSingle(buffer, i * floatWidth);
                    }

                    Thread.Sleep(10);
                }
            }
            catch (SocketException)
            {
                _connected = false;
                try { socket?.Close(); } catch { }
                Debug.LogWarning("Disconnection detected! Reconnecting in 1s.");
                Thread.Sleep(1000);
            }
        }
    }

    public void OnEditHostIpButtonClicked()
    {
        var keyboardInputManager = FindObjectOfType<KeyboardInputManager>();
        keyboardInputManager.RequestKeyboardInput(KeyboardInputManager.InputMode.IPAddress, newInput =>
        {
            if (ServerIp != newInput)
            {
                ServerIp = newInput;
                _ipChanged = true;
            }
        });
    }

    public void OnActionButtonClicked()
    {
        _state = _state == State.ArmUp ? State.ArmDown : State.ArmUp;
        lock (_lock)
        {
            _stateChanged = true;
        }
    }

    public void OnSliderAmpUpdated(SliderEventData eventData)
    {
        Amp = eventData.NewValue*40+30;
        lock (_lock)
        {
            _sliderChanged = true;
        }
    }
    public void OnSliderFreqUpdated(SliderEventData eventData)
    {
        Freq = eventData.NewValue*40+90;
     lock (_lock)
        {
            _sliderChanged = true;
        }
    }
    private enum State
    {
        ArmUp,
        ArmDown,
    }
}
