package com.smartparking.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.smartparking.entity.WardEntity;



public interface WardRepository extends MongoRepository<WardEntity, String> {
	List<WardEntity> findByIdDistrict(String id);
}
