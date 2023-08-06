

def _format_bytes(size: int):
    """
    Format bytes to human readable format.

    Thanks to: https://stackoverflow.com/a/70211279
    """
    power_labels = {40: "TB", 30: "GB", 20: "MB", 10: "KB"}
    for power, label in power_labels.items():
        if size >= 2 ** power:
            approx_size = size / 2 ** power
            return f"{approx_size:.1f} {label}"
    return f"{size} bytes"

css = '''<style>
.details {user-select: none;}
.details>summary .span.icon {width: 24px;height: 24px;transition: all 0.3s;margin-left: auto;}
.details[open].summary.span.icon{transform:rotate(180deg);}
.summary{display:flex;cursor:pointer;} 
.summary::-webkit-details-marker{display:none;}
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}
.tooltip .tooltiptext {
  visibility: hidden;
  width: 165px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 4px;
  padding: 2px 0;
  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  font-size: 11px;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
}
.tooltip-top {
 bottom: 90%;
 margin-left: -40px;
 }
</style>'''
