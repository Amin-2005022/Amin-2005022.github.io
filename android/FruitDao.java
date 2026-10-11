package com.example.database;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;

import java.util.List;

@Dao
public interface FruitDao {
    @Insert
    void insert(Fruit fruit);

    @Delete
    void delete(Fruit fruit);

    @Query("SELECT * FROM Fruit")
    List<Fruit> getAll();
}