var styles = [ {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.6.0",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "default",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 2.0,
      "color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "background-color" : "rgb(255,255,255)",
      "border-opacity" : 1.0,
      "shape" : "ellipse",
      "width" : 60.0,
      "text-opacity" : 1.0,
      "height" : 40.0,
      "border-color" : "rgb(0,0,0)",
      "background-opacity" : 1.0,
      "font-size" : 12,
      "text-valign" : "center",
      "text-halign" : "center",
      "content" : "data(shared_name)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "text-valign" : "bottom"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "color" : "rgb(0,102,204)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "background-color" : "rgb(255,255,255)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "border-color" : "rgb(0,102,204)"
    }
  }, {
    "selector" : "node[Node_Type = 'Antigen']",
    "css" : {
      "shape" : "triangle"
    }
  }, {
    "selector" : "node[Node_Type = 'EffectorMolecule']",
    "css" : {
      "shape" : "roundrectangle"
    }
  }, {
    "selector" : "node[Node_Type = 'Antibody']",
    "css" : {
      "shape" : "v"
    }
  }, {
    "selector" : "node[Node_Type = 'Cytokine']",
    "css" : {
      "shape" : "diamond"
    }
  }, {
    "selector" : "node[Node_Type = 'Cell']",
    "css" : {
      "shape" : "ellipse"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "text-opacity" : 1.0,
      "source-arrow-shape" : "none",
      "font-size" : 10,
      "target-arrow-color" : "rgb(0,0,0)",
      "content" : "",
      "target-arrow-shape" : "triangle",
      "opacity" : 1.0,
      "width" : 1.0,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "color" : "rgb(0,0,0)",
      "line-style" : "solid",
      "source-arrow-color" : "rgb(0,0,0)",
      "line-color" : "rgb(64,64,64)"
    }
  }, {
    "selector" : "edge[interaction = 'Inhibit']",
    "css" : {
      "line-style" : "dashed"
    }
  }, {
    "selector" : "edge[interaction = 'Differentiate']",
    "css" : {
      "line-style" : "dashed"
    }
  }, {
    "selector" : "edge[interaction = 'Secrete']",
    "css" : {
      "line-style" : "dotted"
    }
  }, {
    "selector" : "edge[interaction = 'Activate']",
    "css" : {
      "line-style" : "dashed"
    }
  }, {
    "selector" : "edge[interaction = 'Survive']",
    "css" : {
      "line-style" : "dashed"
    }
  }, {
    "selector" : "edge[interaction = 'Kill']",
    "css" : {
      "line-style" : "dashed"
    }
  }, {
    "selector" : "edge[interaction = 'Polarize']",
    "css" : {
      "line-style" : "dashed"
    }
  }, {
    "selector" : "edge[interaction = 'Recruit']",
    "css" : {
      "line-style" : "dashed"
    }
  }, {
    "selector" : "edge[interaction = 'Inhibit']",
    "css" : {
      "target-arrow-color" : "rgb(255,0,0)"
    }
  }, {
    "selector" : "edge[interaction = 'Secrete']",
    "css" : {
      "target-arrow-color" : "rgb(204,51,255)"
    }
  }, {
    "selector" : "edge[interaction = 'Differentiate']",
    "css" : {
      "target-arrow-color" : "rgb(153,153,153)"
    }
  }, {
    "selector" : "edge[interaction = 'Activate']",
    "css" : {
      "target-arrow-color" : "rgb(0,204,0)"
    }
  }, {
    "selector" : "edge[interaction = 'Survive']",
    "css" : {
      "target-arrow-color" : "rgb(0,204,0)"
    }
  }, {
    "selector" : "edge[interaction = 'Kill']",
    "css" : {
      "target-arrow-color" : "rgb(255,0,0)"
    }
  }, {
    "selector" : "edge[interaction = 'Recruit']",
    "css" : {
      "target-arrow-color" : "rgb(0,204,0)"
    }
  }, {
    "selector" : "edge[interaction = 'Polarize']",
    "css" : {
      "target-arrow-color" : "rgb(153,153,153)"
    }
  }, {
    "selector" : "edge[interaction = 'Inhibit']",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  }, {
    "selector" : "edge[interaction = 'Differentiate']",
    "css" : {
      "line-color" : "rgb(153,153,153)"
    }
  }, {
    "selector" : "edge[interaction = 'Secrete']",
    "css" : {
      "line-color" : "rgb(204,51,255)"
    }
  }, {
    "selector" : "edge[interaction = 'Activate']",
    "css" : {
      "line-color" : "rgb(0,204,0)"
    }
  }, {
    "selector" : "edge[interaction = 'Survive']",
    "css" : {
      "line-color" : "rgb(0,204,0)"
    }
  }, {
    "selector" : "edge[interaction = 'Kill']",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  }, {
    "selector" : "edge[interaction = 'Polarize']",
    "css" : {
      "line-color" : "rgb(153,153,153)"
    }
  }, {
    "selector" : "edge[interaction = 'Recruit']",
    "css" : {
      "line-color" : "rgb(0,204,0)"
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.6.0",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Basic",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 2.0,
      "color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "background-color" : "rgb(255,255,255)",
      "border-opacity" : 1.0,
      "shape" : "ellipse",
      "width" : 60.0,
      "text-opacity" : 1.0,
      "height" : 40.0,
      "border-color" : "rgb(0,0,0)",
      "background-opacity" : 1.0,
      "font-size" : 12,
      "text-valign" : "center",
      "text-halign" : "center",
      "content" : "data(shared_name)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "text-valign" : "bottom"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "color" : "rgb(0,102,204)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "background-color" : "rgb(255,255,255)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "border-color" : "rgb(0,102,204)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "shape" : "rectangle"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "text-opacity" : 1.0,
      "source-arrow-shape" : "none",
      "font-size" : 10,
      "target-arrow-color" : "rgb(0,0,0)",
      "content" : "",
      "target-arrow-shape" : "none",
      "opacity" : 1.0,
      "width" : 1.0,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "color" : "rgb(0,0,0)",
      "line-style" : "solid",
      "source-arrow-color" : "rgb(0,0,0)",
      "line-color" : "rgb(64,64,64)"
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}]