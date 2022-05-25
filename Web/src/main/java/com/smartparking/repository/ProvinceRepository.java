package com.smartparking.repository;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.smartparking.entity.ProvinceEntity;

public interface ProvinceRepository extends MongoRepository<ProvinceEntity, String>{

}
