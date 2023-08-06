function onCollapseToggled(sender)
{
    let child = sender.children.length > 0 ? sender.children[0] : null;

    if(child != null)
    {
        if(sender.classList.contains("collapsed"))
        {
            child.classList.remove("fa-chevron-up");
            child.classList.add("fa-chevron-down");
        }
        else
        {
            child.classList.remove("fa-chevron-down");
            child.classList.add("fa-chevron-up");
        }
    }
}
