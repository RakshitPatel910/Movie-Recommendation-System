import express from "express";
import { getContentBasedRec } from "../controllers/recommendController.js";

const router = express.Router()

router.post('/getContentBasedRec', getContentBasedRec);   

export default router;