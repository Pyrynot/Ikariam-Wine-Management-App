import React from 'react';
import { deleteTown } from '../api';

function TownDeleteButton({ townId, onDeleteSuccess, fetchAndUpdateTowns }) {
    const handleDeleteClick = async () => {
      const isConfirmed = window.confirm("Are you sure you want to delete this town?");
      if (isConfirmed) {
        try {
          await deleteTown(townId);
          onDeleteSuccess();  // You might reconsider the need of this if fetchAndUpdateTowns() is enough
          fetchAndUpdateTowns();  // Refresh the list from the server
        } catch (error) {
          console.error('Deletion failed:', error);
        }
      }
    };
  
    return (
      <button onClick={handleDeleteClick} className="delete-button">
        Delete
      </button>
    );
  }
  
  export default TownDeleteButton;