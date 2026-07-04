import { useEffect, useState } from "react"
import axios from "axios"


export default function TodoPage() {
    // 리액트가 실행될때의 순서
    // 컴포넌트 시작 -> useState 생성 -> useEffect 등록 ->렌더링 -> getTodo 실행

    const [todo, setTodo] = useState(null);
    //var response = await axios.get("https://jsonplaceholder.typicode.com/todos/90")
    //쿼리스트링으로 요청보내는 방식 var response = await axios.get("https://jsonplaceholder.typicode.com/todo?id=1")

    // window.location.search는 URL에서 "?id=1" 부분만 가져옵니다.
    const searchParams = new URLSearchParams(window.location.search);

    // 'id' 키의 값을 추출하여 상태에 저장합니다.
    const currentId = searchParams.get('id');


    const getTodo = async () => {
        var response = await axios.get('https://jsonplaceholder.typicode.com/todos/' + currentId);
        var todo = response.data;
        setTodo(todo);
    }

    useEffect(() => {
        getTodo()
    }, []);

    //ui가 바뀌어야한다면 무조건 useState를 쓴다
    // const [title, setTitle] = useState('');
    // const [id, setId] = useState('');
    // const [userId, setUserId] = useState('');
    // const [completed, setCompleted] = useState('');

    return (
        <div>
            <h1>TodoPage</h1>
            <p>title : {todo?.title}</p>
            <p>id : {todo?.id}</p>
            <p>userId : {todo?.userId}</p>
            <p>completed : {todo?.completed ? "완료" : "미완료"}</p>
        </div>
    )
}
