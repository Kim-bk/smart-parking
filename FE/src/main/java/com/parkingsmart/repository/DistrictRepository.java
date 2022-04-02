package com.parkingsmart.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.parkingsmart.entity.DistrictEntity;
import com.parkingsmart.entity.ProvinceEntity;

public interface DistrictRepository extends JpaRepository<DistrictEntity, String>{
	
	List<DistrictEntity> findByProvince(ProvinceEntity province);

}
