const express = require("express");
const fs = require("fs");
const router = express.Router();
const { visit } = require("../helpers/botHelper");

router.get("/", (req, res) => {
  return res.render("home.html");
});

router.post("/search", (req, res) => {
  const { query } = req.body;

  if (query) {
    try {
      visit(query);

      return res.status(200).json({ message: "Bot triggered successfully." });
    } catch (err) {
      return res.status(500).json({ message: "Error triggering bot.", error: err.message });
    }
  } else {
    return res.status(400).json({ message: "No search query provided." });
  }
});

module.exports = () => {
  return router;
};
