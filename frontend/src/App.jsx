import React, { useEffect, useState } from 'react';
import './App.css';
import { fetchTowns } from './api'; 
import DisplayTowns from './components/DisplayTowns'; 
import NewTownForm from './components/NewTownForm';
import TransferWineForm from './components/TransferWineForm';

const BACKEND_URL = "http://localhost:8000";

function App() {
  const [towns, setTowns] = useState([]);
  const [uniquePlayerNames, setUniquePlayerNames] = useState([]);
  const [playerName, setPlayerName] = useState('');
  const [playerTowns, setPlayerTowns] = useState([]);
  

  useEffect(() => {
    const fetchAndSetTowns = async () => {
      const townsData = await fetchTowns(BACKEND_URL);
      setTowns(townsData);
      setUniquePlayerNames([...new Set(townsData.map(town => town.player_name))]);
    };
    fetchAndSetTowns();
  }, []);


  useEffect(() => {
    const filteredTowns = towns.filter(town => town.player_name === playerName);
    setPlayerTowns(filteredTowns);
  }, [playerName, towns]);


  const fetchAndUpdateTowns = async () => {
    try {
      const fetchedTowns = await fetchTowns(BACKEND_URL); // Ensure this matches your API expectations
      setTowns(fetchedTowns);
      // Update player towns if needed
      const filteredTowns = fetchedTowns.filter(town => town.player_name === playerName);
      setPlayerTowns(filteredTowns);
    } catch (error) {
      console.error('Failed to fetch towns:', error);
    }
  };



  // Handlers for UI actions

  return (
    <div className="App">
      <h1>Ikariam wine management system</h1>
      {/* ...other components */}
      <NewTownForm onNewTownAdded={fetchAndUpdateTowns}/>
      <TransferWineForm playerName={playerName} towns={towns} onTransferSuccess={fetchAndUpdateTowns} />
      <DisplayTowns towns={towns} fetchAndUpdateTowns={fetchAndUpdateTowns}/> {/* Add DisplayTowns component here */}
    </div>
  );
}

export default App;