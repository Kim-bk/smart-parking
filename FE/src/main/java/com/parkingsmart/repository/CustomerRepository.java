package com.parkingsmart.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.parkingsmart.entity.CustomerEntity;

public interface CustomerRepository extends JpaRepository<CustomerEntity, String>{

}
