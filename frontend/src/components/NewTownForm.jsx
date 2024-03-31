import React, { useState } from 'react';
import { addTown } from '../api';
import './FormStyles.css';

const NewTownForm = ({ onNewTownAdded }) => {
  const [newPlayerName, setNewPlayerName] = useState('');
  const [newTownName, setNewTownName] = useState('');
  const [newWineStorage, setNewWineStorage] = useState(0);
  const [newWineHourlyConsumption, setNewWineHourlyConsumption] = useState(0);
  const [newWineProduction, setNewWineProduction] = useState(0);

  const handleAddNewTown = async (event) => {
    event.preventDefault();
    try {
        await addTown(newPlayerName, newTownName, newWineStorage, newWineHourlyConsumption, newWineProduction);
        alert('New town added successfully');
        onNewTownAdded(); // Call the function passed via props to refresh the towns list.
        // Optionally clear the form fields here
        setNewPlayerName('');
        setNewTownName('');
        setNewWineStorage(0);
        setNewWineHourlyConsumption(0);
        setNewWineProduction(0);
      } catch (error) {
        alert('Failed to add new town: ' + error.message);
      }
    };

    return (
        <form onSubmit={handleAddNewTown} className="new-town-form">
          <div className="form-field">
            <label htmlFor="playerName">Player Name</label>
            <input
              id="playerName"
              type="text"
              value={newPlayerName}
              onChange={(e) => setNewPlayerName(e.target.value)}
              required
            />
          </div>
          <div className="form-field">
            <label htmlFor="townName">Town Name</label>
            <input
              id="townName"
              type="text"
              value={newTownName}
              onChange={(e) => setNewTownName(e.target.value)}
              required
            />
          </div>
          <div className="form-field">
            <label htmlFor="wineStorage">Wine Storage</label>
            <input
              id="wineStorage"
              type="number"
              value={newWineStorage}
              onChange={(e) => setNewWineStorage(e.target.value)}
              min="0"
              step="0.01"
              required
            />
          </div>
          <div className="form-field">
            <label htmlFor="wineHourlyConsumption">Hourly Consumption</label>
            <input
              id="wineHourlyConsumption"
              type="number"
              value={newWineHourlyConsumption}
              onChange={(e) => setNewWineHourlyConsumption(e.target.value)}
              min="0"
              step="0.01"
              required
            />
          </div>
          <div className="form-field">
            <label htmlFor="wineProduction">Wine Production</label>
            <input
              id="wineProduction"
              type="number"
              value={newWineProduction}
              onChange={(e) => setNewWineProduction(e.target.value)}
              min="0"
              step="0.01"
              required
            />
          </div>
          <button type="submit" className="submit-button">Add New Town</button>
        </form>
      );
};

export default NewTownForm;
