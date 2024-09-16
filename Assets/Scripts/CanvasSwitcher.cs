using UnityEngine;

public class CanvasSwitcher : MonoBehaviour
{
    public Canvas canvas1;
    public Canvas canvas2;

    public void SwitchCanvas()
    {
        // Toggle the active state of the canvases
        canvas1.gameObject.SetActive(!canvas1.gameObject.activeSelf);
        canvas2.gameObject.SetActive(!canvas2.gameObject.activeSelf);
    }
}
