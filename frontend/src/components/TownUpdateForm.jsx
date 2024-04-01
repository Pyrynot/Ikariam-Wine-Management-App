import React, { useState } from 'react';
import { updateTown } from '../api';

function TownUpdateForm({ town, onUpdateSuccess, onCancel, fetchAndUpdateTowns }) {
    const [formData, setFormData] = useState({
      player_name: town.player_name,
      town_name: town.town_name,
      wine_storage: town.wine_storage,
      wine_hourly_consumption: town.wine_hourly_consumption,
      wine_production: town.wine_production
    });
  
    const handleInputChange = (e) => {
      const { name, value } = e.target;
      setFormData(prevState => ({ ...prevState, [name]: value }));
    };
  
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
          const updatedTown = await updateTown(town.id, formData);
          onUpdateSuccess(updatedTown);  // Assuming this updates the local UI state
          fetchAndUpdateTowns();  // Refresh the list from the server
        } catch (error) {
          console.error('Update failed:', error);
        }
      };
  
    // Form with input fields for town properties
    return (
      <form onSubmit={handleSubmit}>
        <input
          name="town_name"
          value={formData.town_name}
          onChange={handleInputChange}
          placeholder="Town Name"
          required
        />
        <input
          name="wine_storage"
          type="number"
          value={formData.wine_storage}
          onChange={handleInputChange}
          placeholder="Wine Storage"
          required
        />
        <input
          name="wine_hourly_consumption"
          type="number"
          value={formData.wine_hourly_consumption}
          onChange={handleInputChange}
          placeholder="Hourly Consumption"
          required
        />
        <input
          name="wine_production"
          type="number"
          value={formData.wine_production}
          onChange={handleInputChange}
          placeholder="Wine Production"
          required
        />
        <button type="submit">Save</button>
        <button type="button" onClick={onCancel}>Cancel</button>
      </form>
    );
  }

  export default TownUpdateForm;