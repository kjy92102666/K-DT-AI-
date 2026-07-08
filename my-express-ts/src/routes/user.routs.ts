import { Router } from 'express';
import { testMethod } from '../controllers/user.controller';
// import { Request, Response } from 'express';

const router = Router();

//컨트롤러에서 이부분을 빼간다. 라우터랑 컨트롤러 분리시키면서 생략.
// router.get('/users', (req: Request, res: Response) => {
//     res.send('Hello, TypeScript with Express!');
// });
router.get('/test', testMethod)

export default router;