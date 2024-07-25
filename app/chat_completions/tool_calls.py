FIND_ELEMENT_TOOL_CALL = {
  "type": "function",
  "function": {
    "name": "find_element",
    "description": "Find an element given a By strategy and locator.",
    "parameters": {
      "type": "object",
      "properties": {
        "by": {
          "type": "string",
          "description": "The strategy to locate the element. Strategies include: "
                         "ID, NAME, CLASS_NAME, TAG_NAME, CSS_SELECTOR, LINK_TEXT, PARTIAL_LINK_TEXT, XPATH"
        },
        "value": {
          "type": "string",
          "description": "The value of the locator. For example, if 'by' is 'ID', "
                         "'value' might be the id of the element."
        }
      },
      "required": ["by", "value"]
    }
  }
}
