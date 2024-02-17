
import './App.css';
import Home from './components/Home';
import Footer from './components/Footer';
import Navbar from './components/Navbar';    
import SignIn from './components/SignIn';
import Signup from './components/Signup'; 
import { Route,Routes,BrowserRouter } from 'react-router-dom';                                            
function App() {
  return (
    <BrowserRouter>
    <div className="App">
      <>
      <Navbar/>
      <Home/>
      <Routes>
        <Route path='/SignIn' element={<SignIn/>}/>
        <Route path='/Signup' element={<Signup/>}/>
      </Routes>
      <Footer/>
      </>
    </div>
    </BrowserRouter>
    
  );
}

export default App;
