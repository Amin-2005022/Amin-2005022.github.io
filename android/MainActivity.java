package com.example.database;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    
    private FruitDao dao;
    private ListView listView;
    
    // We keep a list of the actual database objects to know which one to delete
    private List<Fruit> fruitList;
    // We keep a list of strings to show in the simple ListView
    private List<String> displayNames;
    private ArrayAdapter<String> adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize Database
        AppDatabase db = AppDatabase.getDatabase(this);
        dao = db.fruitDao();

        // Get UI references
        EditText etFruitName = findViewById(R.id.etFruitName);
        Button btnAdd = findViewById(R.id.btnAdd);
        listView = findViewById(R.id.listView);

        // Setup ListView Adapter
        displayNames = new ArrayList<>();
        adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, displayNames);
        listView.setAdapter(adapter);

        // Show data initially
        refreshData();

        // --- ADD BUTTON ---
        btnAdd.setOnClickListener(v -> {
            String name = etFruitName.getText().toString();
            if (!name.isEmpty()) {
                Fruit fruit = new Fruit();
                fruit.name = name;
                
                dao.insert(fruit); // Insert into DB
                
                etFruitName.setText(""); // Clear input
                refreshData(); // Refresh UI
            } else {
                Toast.makeText(this, "Please enter a fruit name", Toast.LENGTH_SHORT).show();
            }
        });

        // --- DELETE ON TAP ---
        listView.setOnItemClickListener((parent, view, position, id) -> {
            // Find which object was tapped using its position in the list
            Fruit fruitToDelete = fruitList.get(position);
            
            dao.delete(fruitToDelete); // Delete from DB
            
            Toast.makeText(this, "Deleted " + fruitToDelete.name, Toast.LENGTH_SHORT).show();
            refreshData(); // Refresh UI
        });
    }

    // Helper method to fetch all records and update the ListView
    private void refreshData() {
        fruitList = dao.getAll();
        
        displayNames.clear();
        for (Fruit f : fruitList) {
            displayNames.add(f.name);
        }
        
        adapter.notifyDataSetChanged(); // Tell the ListView to redraw itself
    }
}