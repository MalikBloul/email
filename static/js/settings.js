let enquirer_input = document.getElementById("enquirer");

enquirer_input.addEventListener("change", function (e) {
  let fetchRes = fetch(`blocks/${e.target.value}`);

  fetchRes
    .then((res) => res.json())
    .then((items) => {
      update_block_input(items);
    });
});

function update_block_input(blocks) {
  let block_inputs = document.getElementById("blocks");

  let child = block_inputs.lastElementChild;

  while (child) {
    block_inputs.removeChild(child);
    child = block_inputs.lastElementChild;
  }

  for (let i = 0; i < blocks.length; i++) {
    let div = document.createElement("div");
    let newInput = document.createElement("input");
    let newLabel = document.createElement("label");

    setAttributes(div, ["class"], ["form-ckeck form-switch"]);

    setAttributes(
      newInput,
      ["type", "class", "value", "id", "name"],
      [
        "checkbox",
        "form-check-input",
        blocks[i]["id"],
        blocks[i]["type"],
        "blocks",
      ]
    );
    setAttributes(
      newLabel,
      ["class", "for"],
      ["form-check-label", blocks[i]["type"]]
    );
    newLabel.innerHTML = blocks[i]["title"];

    div.appendChild(newInput);
    div.appendChild(newLabel);

    block_inputs.appendChild(div);
  }
}

function setAttributes(ele, attributes, settings) {
  for (let i = 0; i < attributes.length; i++) {
    ele.setAttribute(attributes[i], settings[i]);
  }
}
