import logo from './logo.svg';
import './App.css';

function handleFetch(){
  fetch('https://dummyjson.com/products/1')
  .then(res => res.json())
  .then(json => console.log(json))
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h2>Rum Headers Example</h2>
        <img src={logo} className="App-logo" alt="logo" />
        <button className="button" onClick={handleFetch}>Submit Fetch Request</button>
      </header>
    </div>
  );
}

export default App;
