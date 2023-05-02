using Microsoft.MixedReality.Toolkit.UI;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class TouchSliderValue : MonoBehaviour
{
    public float start;
    public float range;
    public string unit="";
    [AddComponentMenu("Scripts/MRTK/Examples/TouchSliderValue")]
    [SerializeField]
    private TextMeshPro textMesh = null;

    public void OnSliderUpdated_scaled(SliderEventData eventData)
    {

        if (textMesh == null)
        {
            textMesh = GetComponent<TextMeshPro>();
        }

        if (textMesh != null)
        {
            textMesh.text = $"{start + range * eventData.NewValue:N}"+unit;
        }
    }
    // public void SliderDataTransmitter(SliderEventData eventData)
    // { }
}
