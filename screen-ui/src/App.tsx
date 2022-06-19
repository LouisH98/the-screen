import { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);
  return (
    <div className="bg-white h-screen dark:bg-stone-900">
      <button onClick={() => setCount(count + 1)}>
        Click me pls
      </button>
      <h1 className="text-3xl dark:text-white font-bold underline">Hello World! {count}</h1>
    </div>
  );
}

export default App;
 