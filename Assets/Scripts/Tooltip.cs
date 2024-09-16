using UnityEngine;
using UnityEngine.UI;

public class Tooltip : MonoBehaviour
{
    public Text tooltipText;
    public RectTransform backgroundRectTransform;

    private void Start()
    {
        HideTooltip();
    }

    private void Update()
    {
        Vector2 localPoint;
        RectTransformUtility.ScreenPointToLocalPointInRectangle(
            transform.parent.GetComponent<RectTransform>(),
            Input.mousePosition,
            null,
            out localPoint);
        transform.localPosition = localPoint;
    }

    public void ShowTooltip(string tooltipString)
    {
        gameObject.SetActive(true);
        tooltipText.text = tooltipString;
        Vector2 backgroundSize = new Vector2(tooltipText.preferredWidth + 8f, tooltipText.preferredHeight + 8f);
        backgroundRectTransform.sizeDelta = backgroundSize;
    }

    public void HideTooltip()
    {
        gameObject.SetActive(false);
    }
}
