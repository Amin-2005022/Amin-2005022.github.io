package com.example.database;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity
public class Fruit {
    @PrimaryKey(autoGenerate = true)
    public int id;
    
    public String name;
}