const { generatePDF } = require("../utils/exporter");
const { isAuthenticated, isAdmin } = require("../middlewares");
const { rotatePass, verifyPass } = require("../utils/pass");
const { NodeHtmlMarkdown } = require("node-html-markdown");
const { findDocument } = require("../database");

const nhm = new NodeHtmlMarkdown();

const router = require("express").Router();

router.get(
  "/document/export/:id",
  isAuthenticated,
  isAdmin,
  async (req, res) => {
    const { id } = req.params;
    const user = req.user;
    const document = findDocument(user.id, id);
    if (!document) return res.status(404).send("Document not found");
    console.log("Document found:", document);
    const content = nhm.translate(document.content);
    console.log("content",content);
    const generatedPDF = await generatePDF(content);

    res.set("Content-disposition", "attachment; filename=generated.pdf");
    res.set("Content-Type", "application/pdf");
    return res.send(generatedPDF);
  },
);

router.post("/document/debug/export", isAuthenticated, isAdmin, async (req, res) => {
  const { access_pass, content } = req.body;
  console.log("Access pass received:", access_pass);
  console.log("Content length:", content.length);

  if (!verifyPass(access_pass)) {
    rotatePass();
    return res.status(403).send("BAD PASS, WHO ARE YOU STRANGER ?!");
  }

  res.set("Content-disposition", "attachment; filename=generated.pdf");
  res.set("Content-Type", "application/pdf");

  const generatedPDF = await generatePDF(content);

  return res.send(generatedPDF);
});

module.exports = router;
