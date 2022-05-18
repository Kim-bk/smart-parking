package com.smartparking.repository;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.smartparking.entity.AddressEntity;


public interface AddressRepository extends MongoRepository<AddressEntity, Long>{

}
