package com.smartparking.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.smartparking.entity.DistrictEntity;

public interface DistrictRepository extends MongoRepository<DistrictEntity, String>{
	
	
	List<DistrictEntity> findByIdProvince(String id);

}
