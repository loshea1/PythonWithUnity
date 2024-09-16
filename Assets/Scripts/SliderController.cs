using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class SliderController : MonoBehaviour
{
    public TMP_Text valueText;
    public Slider slider;
    public float increment = 0.05f;

    void Start()
    {
        // Set the initial value and update the text
        OnSliderChanged(slider.value);
    }

    public void OnSliderChanged(float value)
    {
        // Round the value to the nearest increment
        float roundedValue = Mathf.Round(value / increment) * increment;
        slider.value = roundedValue;

        // Update the text to display the rounded value with the appropriate format
        valueText.text = roundedValue.ToString("F" + GetDecimalPlaces(increment));
    }

    private int GetDecimalPlaces(float value)
    {
        int decimalPlaces = 0;
        while (value < 1)
        {
            decimalPlaces++;
            value *= 10;
        }
        return decimalPlaces;
    }
}
