import express, { Request, Response } from 'express';
import userRoutes from './routes/user.routs';
import cors from 'cors';

const app = express();
const port = 3000;

//cors
app.use(cors());

//json 설정
app.use(express.json());
app.use(express.urlencoded({ extended: true }));



app.use('/api/user', userRoutes);


app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
