using UnityEngine;
using UnityEngine.EventSystems;

public class UIElementWithTooltip : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{
    public string tooltipText;
    private Tooltip tooltip;

    private void Start()
    {
        tooltip = FindObjectOfType<Tooltip>();
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
        tooltip.ShowTooltip(tooltipText);
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        tooltip.HideTooltip();
    }
}
