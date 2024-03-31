import React, { useState, useEffect } from 'react';
import { transferWine } from '../api';

const TransferWineForm = ({ towns, onTransferSuccess }) => {
  const [selectedPlayerName, setSelectedPlayerName] = useState('');
  const [sourceTown, setSourceTown] = useState('');
  const [destinationTown, setDestinationTown] = useState('');
  const [wineAmount, setWineAmount] = useState('');
  const [playerNames, setPlayerNames] = useState([]);

  useEffect(() => {
    setPlayerNames([...new Set(towns.map(town => town.player_name))]);
  }, [towns]);

  const handleTransferWine = async (event) => {
    event.preventDefault();
    try {
      const result = await transferWine(selectedPlayerName, sourceTown, destinationTown, wineAmount);
      console.log('Transfer successful:', result);
      alert('Wine transferred successfully!');
      onTransferSuccess(); // This should be a function passed from the parent component to refresh the towns
      setSourceTown('');
      setDestinationTown('');
      setWineAmount('');
    } catch (error) {
      alert('Failed to transfer wine. Error: ' + error.message);
    }
  };

  return (
    <form onSubmit={handleTransferWine} className="transfer-wine-form">
      <h3>Transfer Wine</h3>
      <select value={selectedPlayerName} onChange={(e) => setSelectedPlayerName(e.target.value)} required>
        <option value="">Select Player Name</option>
        {playerNames.map((playerName) => (
          <option key={playerName} value={playerName}>{playerName}</option>
        ))}
      </select>
      <select value={sourceTown} onChange={(e) => setSourceTown(e.target.value)} required>
        <option value="">Select Source Town</option>
        {towns.filter(town => town.player_name === selectedPlayerName).map((town) => (
          <option key={town.id} value={town.town_name}>{town.town_name}</option>
        ))}
      </select>
      <select value={destinationTown} onChange={(e) => setDestinationTown(e.target.value)} required>
        <option value="">Select Destination Town</option>
        {towns.filter(town => town.player_name === selectedPlayerName && town.town_name !== sourceTown).map((town) => (
          <option key={town.id} value={town.town_name}>{town.town_name}</option>
        ))}
      </select>
      <input
        type="number"
        value={wineAmount}
        onChange={(e) => setWineAmount(e.target.value)}
        placeholder="Amount of Wine"
        min="0"
        required
      />
      <button type="submit">Transfer Wine</button>
    </form>
  );
};

export default TransferWineForm;
