import { useState } from 'react';
import axios from 'axios'; 
import './App.css';

function App() {
  const [input, setInput] = useState('')
  // const [movieInput, setMovieInput] = useState([])
  const [result, setResult] = useState([])

  const getRecommendation = async (movieInput) => {
    console.log(movieInput)
    await axios.post('http://localhost:3010/getRecommendation/getContentBasedRec', { input_movies: movieInput})
      .then((res) => {
        console.log(res.data.recommendationList);
        setResult(res.data.recommendationList)
      })
      .catch((err) => {
        console.log(err);
      })
  }

  const handleSubmit = async () => {
    let list = await input.replaceAll(', ', ',');

    let finalList = await list.split(',');

    // setMovieInput(movieInput.concat(finalList));
    console.log(finalList);

    await getRecommendation(finalList);
  }

  return (
    <>
      <div style={{ display:'flex', flexDirection:'column', justifyContent:'center', alignItems: 'center' }}>
        <input 
        type='text' 
        onChange={(e) => {setInput(e.target.value)}}
        style={{ padding:'5px',width: '70vw', }} ></input>
        {/* {console.log(input)} */}
        <button onClick={() => handleSubmit()} style={{ padding:'20px', margin: '20px', border:'2px solid white' }}  >Submit</button>
      </div>
      {
        result.map( (movie) => (
            <p> {movie} </p>
         ) )
      }
    </>
  )
}

export default App
