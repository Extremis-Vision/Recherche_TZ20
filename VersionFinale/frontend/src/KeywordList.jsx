import React, { useState } from 'react';

const KeywordList = ({ keywords, setKeywords }) => {
  const [editingKeywordIndex, setEditingKeywordIndex] = useState(null);
  const [editingKeywordValue, setEditingKeywordValue] = useState('');
  const [addingKeyword, setAddingKeyword] = useState(false);
  const [newKeyword, setNewKeyword] = useState('');

  const handleDeleteKeyword = (index) => {
    setKeywords((prevKeywords) => prevKeywords.filter((_, i) => i !== index));
    if (editingKeywordIndex === index) {
      setEditingKeywordIndex(null);
      setEditingKeywordValue('');
    }
  };

  const handleEditKeyword = (index) => {
    setEditingKeywordIndex(index);
    setEditingKeywordValue(keywords[index]);
  };

  const handleEditKeywordSubmit = (e) => {
    e.preventDefault();
    if (editingKeywordValue.trim() === '') return;
    setKeywords((prevKeywords) =>
      prevKeywords.map((kw, i) =>
        i === editingKeywordIndex ? editingKeywordValue.trim() : kw
      )
    );
    setEditingKeywordIndex(null);
    setEditingKeywordValue('');
  };

  const handleEditKeywordCancel = () => {
    setEditingKeywordIndex(null);
    setEditingKeywordValue('');
  };

  const handleAddKeyword = (e) => {
    e.preventDefault();
    const value = newKeyword.trim();
    if (!value) return;
    if (keywords && keywords.includes(value)) {
      setNewKeyword('');
      setAddingKeyword(false);
      return;
    }
    setKeywords((prevKeywords) => (prevKeywords ? [...prevKeywords, value] : [value]));
    setNewKeyword('');
    setAddingKeyword(false);
  };

  return (
    <div>
      {keywords && (
        <div className="result" style={{ marginBottom: '1em' }}>
          <h2>Mots-clés générés :</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5em', alignItems: 'center' }}>
            {keywords.map((keyword, index) =>
              editingKeywordIndex === index ? (
                <form
                  key={index}
                  onSubmit={handleEditKeywordSubmit}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    background: '#e0e0e0',
                    borderRadius: '16px',
                    padding: '0.2em 0.6em',
                  }}
                >
                  <input
                    type="text"
                    value={editingKeywordValue}
                    autoFocus
                    onChange={(e) => setEditingKeywordValue(e.target.value)}
                    style={{
                      border: 'none',
                      outline: 'none',
                      background: 'transparent',
                      fontSize: '1em',
                      width: '7em',
                    }}
                  />
                  <button
                    type="submit"
                    style={{
                      marginLeft: '0.3em',
                      border: 'none',
                      background: 'transparent',
                      cursor: 'pointer',
                      color: 'green',
                      fontWeight: 'bold',
                    }}
                    title="Valider"
                  >
                    ✓
                  </button>
                  <button
                    type="button"
                    onClick={handleEditKeywordCancel}
                    style={{
                      marginLeft: '0.1em',
                      border: 'none',
                      background: 'transparent',
                      cursor: 'pointer',
                      color: 'red',
                      fontWeight: 'bold',
                    }}
                    title="Annuler"
                  >
                    ✗
                  </button>
                </form>
              ) : (
                <span
                  key={index}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    background: '#e0e0e0',
                    borderRadius: '16px',
                    padding: '0.2em 0.6em',
                    cursor: 'pointer',
                    fontSize: '1em',
                  }}
                  onClick={() => handleEditKeyword(index)}
                  title="Cliquez pour modifier"
                >
                  {keyword}
                  <span
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteKeyword(index);
                    }}
                    style={{
                      marginLeft: '0.4em',
                      color: '#b71c1c',
                      fontWeight: 'bold',
                      cursor: 'pointer',
                      fontSize: '1.1em',
                    }}
                    title="Supprimer"
                  >
                    ×
                  </span>
                </span>
              )
            )}
            {addingKeyword ? (
              <form
                onSubmit={handleAddKeyword}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  background: '#e0e0e0',
                  borderRadius: '16px',
                  padding: '0.2em 0.6em',
                  marginLeft: '0.5em',
                }}
              >
                <input
                  type="text"
                  value={newKeyword}
                  autoFocus
                  onChange={(e) => setNewKeyword(e.target.value)}
                  style={{
                    border: 'none',
                    outline: 'none',
                    background: 'transparent',
                    fontSize: '1em',
                    width: '7em',
                  }}
                  placeholder="Nouveau mot-clé"
                />
                <button
                  type="submit"
                  style={{
                    marginLeft: '0.3em',
                    border: 'none',
                    background: 'transparent',
                    cursor: 'pointer',
                    color: 'green',
                    fontWeight: 'bold',
                  }}
                  title="Ajouter"
                >
                  ✓
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setAddingKeyword(false);
                    setNewKeyword('');
                  }}
                  style={{
                    marginLeft: '0.1em',
                    border: 'none',
                    background: 'transparent',
                    cursor: 'pointer',
                    color: 'red',
                    fontWeight: 'bold',
                  }}
                  title="Annuler"
                >
                  ✗
                </button>
              </form>
            ) : (
              <button
                type="button"
                onClick={() => setAddingKeyword(true)}
                style={{
                  marginLeft: '0.5em',
                  border: 'none',
                  background: '#e0e0e0',
                  borderRadius: '16px',
                  padding: '0.2em 0.6em',
                  cursor: 'pointer',
                  fontSize: '1em',
                  color: '#1976d2',
                  fontWeight: 'bold',
                }}
                title="Ajouter un mot-clé"
              >
                + Ajouter un mot-clé
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default KeywordList;
