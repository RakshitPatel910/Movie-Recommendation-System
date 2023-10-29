import express from "express";
import cors from 'cors'
import bodyParser from'body-parser';
import recommend from './router/recommend.js';

const app = express();

app.use(express.json());
app.use(express.urlencoded({ limit: "30mb", extended: true })) // to convert incoming data in express to json
app.use(cors());

app.use("/getRecommendation", recommend)

const port = '3010';

app.listen(port, () => {
  console.log("server is running at port 3010");
});